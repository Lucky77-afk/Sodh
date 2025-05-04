import React, { useState, useEffect } from 'react';
import { View, StyleSheet, ScrollView, TouchableOpacity, ActivityIndicator, RefreshControl } from 'react-native';
import { Text, Card, TextInput, Button, useTheme, Divider } from 'react-native-paper';
import { useWallet } from '../context/WalletContext';
import { getAccountInfo, getAccountTransactions } from '../services/solana-service';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import { useNavigation } from '@react-navigation/native';
import { Connection, clusterApiUrl } from '@solana/web3.js';
import * as Clipboard from 'expo-clipboard';
import { StackNavigationProp } from '@react-navigation/stack';

type AccountScreenProps = {};

const AccountScreen: React.FC<AccountScreenProps> = () => {
  const theme = useTheme();
  const navigation = useNavigation<StackNavigationProp<any>>();
  const { connected, walletAddress, balance, connectWallet, disconnectWallet } = useWallet();
  
  const [addressInput, setAddressInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [refreshing, setRefreshing] = useState(false);
  const [accountData, setAccountData] = useState<any>(null);
  const [transactions, setTransactions] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);

  // Load account data when wallet is connected
  useEffect(() => {
    if (connected && walletAddress) {
      loadAccountData();
    }
  }, [connected, walletAddress]);

  // Load account data from blockchain
  const loadAccountData = async () => {
    if (!walletAddress) return;
    
    setIsLoading(true);
    setError(null);
    
    try {
      // Create connection to Solana devnet
      const connection = new Connection(clusterApiUrl('devnet'));
      
      // Get account info and transactions
      const accountInfo = await getAccountInfo(connection, walletAddress);
      const txs = await getAccountTransactions(connection, walletAddress);
      
      setAccountData(accountInfo);
      setTransactions(txs);
    } catch (err) {
      console.error('Error loading account data:', err);
      setError('Failed to load account data. Please try again.');
    } finally {
      setIsLoading(false);
      setRefreshing(false);
    }
  };

  // Handle refresh
  const onRefresh = () => {
    setRefreshing(true);
    loadAccountData();
  };

  // Handle wallet connection
  const handleConnect = async () => {
    if (!addressInput) {
      setError('Please enter a wallet address');
      return;
    }
    
    setIsLoading(true);
    setError(null);
    
    try {
      await connectWallet(addressInput);
      setAddressInput('');
    } catch (err) {
      console.error('Error connecting wallet:', err);
      setError('Invalid wallet address. Please check and try again.');
    } finally {
      setIsLoading(false);
    }
  };

  // Handle wallet disconnection
  const handleDisconnect = async () => {
    setIsLoading(true);
    try {
      await disconnectWallet();
      setAccountData(null);
      setTransactions([]);
    } catch (err) {
      console.error('Error disconnecting wallet:', err);
    } finally {
      setIsLoading(false);
    }
  };

  // Handle copying wallet address to clipboard
  const copyToClipboard = async () => {
    if (walletAddress) {
      await Clipboard.setStringAsync(walletAddress);
      // Show toast or other notification
    }
  };

  // Handle transaction details navigation
  const openTransactionDetails = (signature: string) => {
    navigation.navigate('TransactionDetails', { signature });
  };

  // If not connected, show connection form
  if (!connected) {
    return (
      <ScrollView 
        style={[styles.container, { backgroundColor: theme.colors.background }]}
        contentContainerStyle={styles.centered}
      >
        <Card style={styles.connectionCard}>
          <Card.Content>
            <Text style={styles.title}>Connect Your Wallet</Text>
            <Text style={styles.subtitle}>Enter a Solana wallet address to explore</Text>
            
            <TextInput
              label="Wallet Address"
              value={addressInput}
              onChangeText={setAddressInput}
              style={styles.input}
              mode="outlined"
              placeholder="Enter Solana wallet address"
              autoCapitalize="none"
              autoCorrect={false}
              error={!!error}
            />
            
            {error && <Text style={[styles.errorText, { color: theme.colors.error }]}>{error}</Text>}
            
            <Button 
              mode="contained" 
              onPress={handleConnect}
              style={styles.connectButton}
              loading={isLoading}
              disabled={isLoading}
            >
              Connect Wallet
            </Button>
            
            <Divider style={styles.divider} />
            
            <Text style={styles.infoText}>
              Note: This is a view-only wallet connection. No private keys are required or stored.
            </Text>
          </Card.Content>
        </Card>
        
        <Card style={styles.exampleCard}>
          <Card.Content>
            <Text style={styles.exampleTitle}>Try These Example Addresses</Text>
            <TouchableOpacity 
              style={styles.exampleItem} 
              onPress={() => setAddressInput('9YDLopW4i6Z8iJAMEUBdJWCiYAmF3NJ87FfCZZ8uUf3S')}
            >
              <Icon name="account" size={20} color={theme.colors.primary} />
              <Text style={styles.exampleAddress}>9YDLopW4i6Z8iJAMEUBdJWCiYAmF3NJ87FfCZZ8uUf3S</Text>
            </TouchableOpacity>
            
            <TouchableOpacity 
              style={styles.exampleItem} 
              onPress={() => setAddressInput('2qXuRJsBfZwRFfXNqbPSofpELBUGkHWdtsfKArwsojAW')}
            >
              <Icon name="account" size={20} color={theme.colors.primary} />
              <Text style={styles.exampleAddress}>2qXuRJsBfZwRFfXNqbPSofpELBUGkHWdtsfKArwsojAW</Text>
            </TouchableOpacity>
          </Card.Content>
        </Card>
      </ScrollView>
    );
  }

  // Connected account view
  return (
    <ScrollView 
      style={[styles.container, { backgroundColor: theme.colors.background }]}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
      }
    >
      {/* Account Overview */}
      <Card style={styles.card}>
        <Card.Title title="Account Overview" />
        <Card.Content>
          {isLoading && !refreshing ? (
            <ActivityIndicator size="large" color={theme.colors.primary} />
          ) : error ? (
            <Text style={{ color: theme.colors.error }}>{error}</Text>
          ) : (
            <View>
              {/* Wallet Address */}
              <Text style={styles.sectionTitle}>WALLET ADDRESS</Text>
              <TouchableOpacity style={styles.addressContainer} onPress={copyToClipboard}>
                <Text style={styles.addressText}>{walletAddress}</Text>
                <Icon name="content-copy" size={16} color="#AAA" />
              </TouchableOpacity>
              
              {/* Balance Cards */}
              <View style={styles.balanceCards}>
                <Card style={[styles.balanceCard, { backgroundColor: theme.colors.surface }]}>
                  <Card.Content>
                    <Text style={styles.balanceLabel}>SOL BALANCE</Text>
                    <Text style={[styles.balanceValue, { color: theme.colors.primary }]}>
                      {accountData?.balance_sol?.toFixed(6) || balance.toFixed(6)}
                    </Text>
                    <Text style={styles.balanceUsd}>
                      ≈ ${(accountData?.balance_sol * 165.32)?.toFixed(2) || (balance * 165.32).toFixed(2)} USD
                    </Text>
                  </Card.Content>
                </Card>
                
                <Card style={[styles.balanceCard, { backgroundColor: theme.colors.surface }]}>
                  <Card.Content>
                    <Text style={styles.balanceLabel}>USDT BALANCE</Text>
                    <Text style={[styles.balanceValue, { color: theme.colors.primary }]}>
                      {accountData?.balance_usdt?.toFixed(2) || '0.00'}
                    </Text>
                    <Text style={styles.balanceUsd}>
                      ≈ ${accountData?.balance_usdt?.toFixed(2) || '0.00'} USD
                    </Text>
                  </Card.Content>
                </Card>
              </View>
              
              {/* Account Stats */}
              <View style={styles.statsContainer}>
                <View style={styles.statItem}>
                  <Text style={styles.statLabel}>Transaction Count</Text>
                  <Text style={styles.statValue}>{accountData?.transaction_count || 0}</Text>
                </View>
                
                <View style={styles.statItem}>
                  <Text style={styles.statLabel}>Token Types</Text>
                  <Text style={styles.statValue}>{accountData?.tokens?.length || 1}</Text>
                </View>
              </View>
              
              {/* Disconnect Button */}
              <Button 
                mode="outlined" 
                onPress={handleDisconnect}
                style={styles.disconnectButton}
                textColor={theme.colors.error}
              >
                Disconnect Wallet
              </Button>
            </View>
          )}
        </Card.Content>
      </Card>

      {/* Recent Transactions */}
      {connected && !isLoading && (
        <Card style={styles.card}>
          <Card.Title 
            title="Recent Transactions" 
            right={(props) => (
              <Button 
                onPress={() => {}} 
                mode="text"
                labelStyle={{ color: theme.colors.primary }}
              >
                View All
              </Button>
            )}
          />
          <Card.Content>
            {transactions.length === 0 ? (
              <Text style={styles.noTransactions}>No recent transactions found for this account</Text>
            ) : (
              transactions.map((tx, index) => (
                <TouchableOpacity 
                  key={index} 
                  style={styles.transactionItem}
                  onPress={() => openTransactionDetails(tx.signature)}
                >
                  <Icon 
                    name={tx.status ? 'check-circle-outline' : 'alert-circle-outline'} 
                    size={24} 
                    color={tx.status ? theme.colors.primary : theme.colors.error} 
                  />
                  <View style={styles.transactionInfo}>
                    <Text style={styles.transactionHash}>
                      {tx.signature.substring(0, 16)}...{tx.signature.substring(tx.signature.length - 4)}
                    </Text>
                    <View style={styles.transactionDetails}>
                      <Text style={styles.transactionType}>{tx.type}</Text>
                      <Text style={[
                        styles.transactionStatus, 
                        { color: tx.status ? theme.colors.primary : theme.colors.error }
                      ]}>
                        {tx.status ? 'Success' : 'Failed'}
                      </Text>
                    </View>
                    <Text style={styles.transactionTime}>
                      {new Date(tx.blockTime * 1000).toLocaleString()}
                    </Text>
                  </View>
                  <Icon name="chevron-right" size={20} color="#AAA" />
                </TouchableOpacity>
              ))
            )}
          </Card.Content>
        </Card>
      )}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
  },
  centered: {
    paddingVertical: 24,
  },
  connectionCard: {
    marginBottom: 16,
    elevation: 4,
  },
  title: {
    fontSize: 24,
    fontWeight: 'bold',
    marginBottom: 8,
    textAlign: 'center',
    color: '#FFFFFF',
  },
  subtitle: {
    fontSize: 16,
    marginBottom: 24,
    textAlign: 'center',
    color: '#AAA',
  },
  input: {
    marginBottom: 8,
  },
  errorText: {
    marginBottom: 16,
  },
  connectButton: {
    marginTop: 8,
  },
  divider: {
    marginVertical: 24,
  },
  infoText: {
    fontSize: 12,
    textAlign: 'center',
    color: '#AAA',
  },
  exampleCard: {
    marginTop: 16,
  },
  exampleTitle: {
    fontSize: 16,
    fontWeight: 'bold',
    marginBottom: 12,
    color: '#CCC',
  },
  exampleItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
    padding: 12,
    backgroundColor: '#1A1A1A',
    borderRadius: 8,
  },
  exampleAddress: {
    marginLeft: 8,
    fontFamily: 'monospace',
    color: '#CCC',
    fontSize: 12,
  },
  card: {
    marginBottom: 16,
    elevation: 4,
  },
  sectionTitle: {
    fontSize: 12,
    color: '#AAA',
    marginBottom: 4,
  },
  addressContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#1A1A1A',
    padding: 12,
    borderRadius: 8,
    marginBottom: 16,
  },
  addressText: {
    flex: 1,
    fontFamily: 'monospace',
    color: '#FFFFFF',
    fontSize: 14,
  },
  balanceCards: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 16,
  },
  balanceCard: {
    width: '48%',
  },
  balanceLabel: {
    fontSize: 12,
    color: '#AAA',
    marginBottom: 4,
  },
  balanceValue: {
    fontSize: 20,
    fontWeight: 'bold',
    marginBottom: 2,
  },
  balanceUsd: {
    fontSize: 12,
    color: '#AAA',
  },
  statsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    backgroundColor: '#1A1A1A',
    padding: 16,
    borderRadius: 8,
    marginBottom: 16,
  },
  statItem: {
    alignItems: 'center',
  },
  statLabel: {
    fontSize: 12,
    color: '#AAA',
    marginBottom: 4,
  },
  statValue: {
    fontSize: 16,
    fontWeight: 'bold',
    color: '#FFFFFF',
  },
  disconnectButton: {
    borderColor: 'rgba(255, 92, 92, 0.3)',
  },
  transactionItem: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 12,
    backgroundColor: '#1A1A1A',
    borderRadius: 8,
    marginBottom: 8,
  },
  transactionInfo: {
    flex: 1,
    marginLeft: 12,
  },
  transactionHash: {
    fontFamily: 'monospace',
    color: '#FFFFFF',
    fontSize: 14,
  },
  transactionDetails: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 4,
  },
  transactionType: {
    color: '#CCC',
    fontSize: 12,
  },
  transactionStatus: {
    fontSize: 12,
  },
  transactionTime: {
    fontSize: 12,
    color: '#AAA',
    marginTop: 2,
  },
  noTransactions: {
    textAlign: 'center',
    color: '#AAA',
    padding: 16,
  },
});

export default AccountScreen;