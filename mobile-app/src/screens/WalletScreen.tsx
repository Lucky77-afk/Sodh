import React, { useState, useEffect } from 'react';
import { View, StyleSheet, ScrollView, RefreshControl, TouchableOpacity } from 'react-native';
import { Card, Title, Paragraph, Button, ActivityIndicator, Divider, Avatar } from 'react-native-paper';
import { useNavigation } from '@react-navigation/native';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import * as Clipboard from 'expo-clipboard';

import { useWallet } from '../context/WalletContext';
import solanaService from '../services/solana-service';
import { NavigationProp, Transaction } from '../types/components';

const WalletScreen = () => {
  const navigation = useNavigation<NavigationProp>();
  const { publicKey, disconnectWallet, isConnected } = useWallet();
  
  const [balance, setBalance] = useState<number | null>(null);
  const [transactions, setTransactions] = useState<Transaction[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [copied, setCopied] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Fetch wallet data
  const fetchWalletData = async () => {
    if (!publicKey) return;
    
    try {
      setError(null);
      // Get SOL balance
      const balanceValue = await solanaService.getBalance(publicKey);
      setBalance(balanceValue);
      
      // Get recent transactions
      const txHistory = await solanaService.getTransactionHistory(publicKey);
      setTransactions(txHistory.slice(0, 10)); // Get first 10 transactions
    } catch (err) {
      console.error('Error fetching wallet data:', err);
      setError('Failed to fetch wallet data. Please try again.');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  // Initial data loading
  useEffect(() => {
    if (isConnected) {
      fetchWalletData();
    } else {
      setLoading(false);
    }
  }, [isConnected, publicKey]);

  // Handle refresh
  const onRefresh = () => {
    setRefreshing(true);
    fetchWalletData();
  };

  // Handle wallet disconnect
  const handleDisconnect = async () => {
    try {
      await disconnectWallet();
      navigation.navigate('Home');
    } catch (err) {
      console.error('Error disconnecting wallet:', err);
    }
  };

  // Copy address to clipboard
  const copyAddressToClipboard = async () => {
    if (publicKey) {
      await Clipboard.setStringAsync(publicKey);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  // Render content based on connection state
  if (!isConnected) {
    return (
      <View style={styles.container}>
        <Card style={styles.card}>
          <Card.Content style={styles.centerContent}>
            <Avatar.Icon 
              size={80} 
              icon="wallet-outline" 
              style={styles.walletIcon} 
              color="#FFFFFF" 
            />
            <Title style={styles.title}>No Wallet Connected</Title>
            <Paragraph style={styles.paragraph}>
              Connect a wallet to view your balances and transactions
            </Paragraph>
            <Button 
              mode="contained" 
              style={styles.button}
              onPress={() => navigation.navigate('ConnectWallet')}
            >
              Connect Wallet
            </Button>
          </Card.Content>
        </Card>
      </View>
    );
  }

  return (
    <ScrollView 
      style={styles.container}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} colors={['#512DA8']} />
      }
    >
      {/* Wallet Address Card */}
      <Card style={styles.card}>
        <Card.Content>
          <View style={styles.addressHeader}>
            <Title style={styles.title}>Wallet</Title>
            <Button 
              mode="text" 
              compact 
              onPress={handleDisconnect}
              style={styles.disconnectButton}
            >
              Disconnect
            </Button>
          </View>
          
          <View style={styles.addressContainer}>
            <Paragraph style={styles.addressLabel}>Address:</Paragraph>
            <TouchableOpacity 
              style={styles.addressValue} 
              onPress={copyAddressToClipboard}
            >
              <Paragraph style={styles.addressText} numberOfLines={1} ellipsizeMode="middle">
                {publicKey}
              </Paragraph>
              <MaterialCommunityIcons 
                name={copied ? "check" : "content-copy"} 
                size={16} 
                color={copied ? "#4CAF50" : "#BDBDBD"} 
              />
            </TouchableOpacity>
          </View>
        </Card.Content>
      </Card>

      {/* Balance Card */}
      <Card style={styles.card}>
        <Card.Content>
          <Title style={styles.title}>Balance</Title>
          {loading ? (
            <ActivityIndicator size="small" color="#512DA8" style={styles.loader} />
          ) : error ? (
            <Paragraph style={styles.error}>{error}</Paragraph>
          ) : (
            <View style={styles.balanceContainer}>
              <View style={styles.tokenBalance}>
                <Avatar.Icon 
                  size={40} 
                  icon="currency-sign" 
                  style={styles.tokenIcon} 
                  color="#FFFFFF" 
                />
                <View style={styles.tokenInfo}>
                  <Paragraph style={styles.tokenName}>SOL</Paragraph>
                  <Title style={styles.tokenValue}>
                    {balance !== null ? balance.toFixed(4) : '0.0000'}
                  </Title>
                </View>
              </View>
            </View>
          )}
        </Card.Content>
      </Card>

      {/* Transaction History Card */}
      <Card style={styles.card}>
        <Card.Content>
          <Title style={styles.title}>Recent Transactions</Title>
          
          {loading ? (
            <ActivityIndicator size="small" color="#512DA8" style={styles.loader} />
          ) : error ? (
            <Paragraph style={styles.error}>{error}</Paragraph>
          ) : transactions.length > 0 ? (
            transactions.map((tx, index) => (
              <View key={index}>
                <TouchableOpacity
                  onPress={() => navigation.navigate('TransactionDetail', { signature: tx.signature })}
                >
                  <View style={styles.transactionItem}>
                    <View style={styles.transactionLeft}>
                      <MaterialCommunityIcons 
                        name="swap-horizontal" 
                        size={24} 
                        color="#7C4DFF" 
                      />
                      <View style={styles.transactionInfo}>
                        <Paragraph style={styles.transactionLabel}>
                          Transaction
                        </Paragraph>
                        <Paragraph style={styles.transactionValue} numberOfLines={1} ellipsizeMode="middle">
                          {tx.signature}
                        </Paragraph>
                      </View>
                    </View>
                    <MaterialCommunityIcons name="chevron-right" size={24} color="#BDBDBD" />
                  </View>
                </TouchableOpacity>
                {index < transactions.length - 1 && <Divider style={styles.divider} />}
              </View>
            ))
          ) : (
            <Paragraph style={styles.emptyMessage}>No transactions found</Paragraph>
          )}
          
          {transactions.length > 0 && (
            <Button 
              mode="text" 
              onPress={() => navigation.navigate('TransactionHistory', { address: publicKey })}
              style={styles.viewAllButton}
            >
              View All Transactions
            </Button>
          )}
        </Card.Content>
      </Card>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1E1E1E',
    padding: 16,
  },
  card: {
    marginBottom: 16,
    backgroundColor: '#2C2C2C',
    borderRadius: 8,
  },
  centerContent: {
    alignItems: 'center',
    padding: 24,
  },
  walletIcon: {
    backgroundColor: '#512DA8',
    marginBottom: 16,
  },
  title: {
    color: '#FFFFFF',
    marginBottom: 12,
  },
  paragraph: {
    color: '#E0E0E0',
    marginBottom: 24,
    textAlign: 'center',
  },
  button: {
    marginTop: 12,
    backgroundColor: '#512DA8',
    width: '80%',
  },
  addressHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  disconnectButton: {
    margin: 0,
    padding: 0,
  },
  addressContainer: {
    marginBottom: 8,
  },
  addressLabel: {
    color: '#BDBDBD',
    marginBottom: 4,
  },
  addressValue: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#3C3C3C',
    borderRadius: 4,
    padding: 8,
  },
  addressText: {
    color: '#E0E0E0',
    flex: 1,
    marginRight: 8,
    fontFamily: 'monospace',
  },
  balanceContainer: {
    marginTop: 8,
  },
  tokenBalance: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 16,
  },
  tokenIcon: {
    backgroundColor: '#512DA8',
    marginRight: 16,
  },
  tokenInfo: {
    flex: 1,
  },
  tokenName: {
    color: '#BDBDBD',
  },
  tokenValue: {
    color: '#FFFFFF',
  },
  loader: {
    marginVertical: 16,
  },
  error: {
    color: '#F44336',
    marginVertical: 16,
  },
  divider: {
    backgroundColor: '#424242',
    height: 1,
    marginVertical: 12,
  },
  transactionItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 12,
  },
  transactionLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  transactionInfo: {
    marginLeft: 12,
    flex: 1,
  },
  transactionLabel: {
    color: '#BDBDBD',
    fontSize: 12,
  },
  transactionValue: {
    color: '#E0E0E0',
  },
  emptyMessage: {
    color: '#BDBDBD',
    fontStyle: 'italic',
    textAlign: 'center',
    marginVertical: 16,
  },
  viewAllButton: {
    marginTop: 8,
  },
});

export default WalletScreen; 