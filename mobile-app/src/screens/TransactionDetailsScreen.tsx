import React, { useState, useEffect } from 'react';
import { View, StyleSheet, ScrollView, ActivityIndicator } from 'react-native';
import { Text, Card, useTheme, Divider, Button } from 'react-native-paper';
import { RouteProp, useRoute, useNavigation } from '@react-navigation/native';
import { Connection, clusterApiUrl } from '@solana/web3.js';
import { getTransactionDetails } from '../services/solana-service';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';
import * as Linking from 'expo-linking';

type RouteParams = {
  TransactionDetails: {
    signature: string;
  };
};

const TransactionDetailsScreen = () => {
  const theme = useTheme();
  const navigation = useNavigation();
  const route = useRoute<RouteProp<RouteParams, 'TransactionDetails'>>();
  const { signature } = route.params;

  const [isLoading, setIsLoading] = useState(true);
  const [transaction, setTransaction] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    loadTransactionData();
  }, [signature]);

  const loadTransactionData = async () => {
    setIsLoading(true);
    setError(null);

    try {
      // Connect to Solana
      const connection = new Connection(clusterApiUrl('devnet'));
      
      // Get transaction details
      const txData = await getTransactionDetails(connection, signature);
      
      if (!txData) {
        throw new Error('Transaction not found');
      }
      
      setTransaction(txData);
    } catch (err) {
      console.error('Error loading transaction:', err);
      setError('Failed to load transaction details. Please try again.');
    } finally {
      setIsLoading(false);
    }
  };

  const openInExplorer = () => {
    Linking.openURL(`https://explorer.solana.com/tx/${signature}?cluster=devnet`);
  };

  if (isLoading) {
    return (
      <View style={[styles.container, styles.centered]}>
        <ActivityIndicator size="large" color={theme.colors.primary} />
        <Text style={{ color: theme.colors.text, marginTop: 16 }}>Loading transaction details...</Text>
      </View>
    );
  }

  if (error || !transaction) {
    return (
      <View style={[styles.container, styles.centered]}>
        <Icon name="alert-circle-outline" size={48} color={theme.colors.error} />
        <Text style={{ color: theme.colors.error, marginTop: 16, textAlign: 'center' }}>
          {error || 'Transaction not found'}
        </Text>
        <Button 
          mode="contained" 
          onPress={() => navigation.goBack()}
          style={{ marginTop: 24 }}
        >
          Go Back
        </Button>
      </View>
    );
  }

  // Format transaction details
  const status = transaction.meta?.err ? 'Failed' : 'Success';
  const statusColor = status === 'Success' ? theme.colors.primary : theme.colors.error;
  const blockTime = transaction.blockTime 
    ? new Date(transaction.blockTime * 1000).toLocaleString()
    : 'Unknown';
  const fee = (transaction.meta?.fee || 0) / 1_000_000_000; // Convert lamports to SOL
  
  // Extract instructions (simplified)
  const instructions = transaction.transaction.message.instructions || [];
  
  // Get account addresses involved
  const accounts = transaction.transaction.message.accountKeys.map((key: any) => key.toString());

  return (
    <ScrollView style={[styles.container, { backgroundColor: theme.colors.background }]}>
      {/* Transaction Header */}
      <Card style={styles.card}>
        <Card.Content>
          <View style={styles.headerRow}>
            <Text style={styles.headerTitle}>Transaction Details</Text>
            <Text style={[styles.statusBadge, { backgroundColor: statusColor }]}>
              {status}
            </Text>
          </View>
          
          <Text style={styles.signatureLabel}>SIGNATURE</Text>
          <Text style={styles.signatureText}>{signature}</Text>
          
          <Button 
            mode="outlined" 
            icon="open-in-new" 
            onPress={openInExplorer}
            style={styles.explorerButton}
          >
            View on Solana Explorer
          </Button>
        </Card.Content>
      </Card>

      {/* Transaction Overview */}
      <Card style={styles.card}>
        <Card.Title title="Overview" />
        <Card.Content>
          <View style={styles.detailRow}>
            <Text style={styles.detailLabel}>Block</Text>
            <Text style={styles.detailValue}>{transaction.slot}</Text>
          </View>
          
          <View style={styles.detailRow}>
            <Text style={styles.detailLabel}>Timestamp</Text>
            <Text style={styles.detailValue}>{blockTime}</Text>
          </View>
          
          <View style={styles.detailRow}>
            <Text style={styles.detailLabel}>Fee</Text>
            <Text style={styles.detailValue}>{fee.toFixed(9)} SOL</Text>
          </View>
          
          <View style={styles.detailRow}>
            <Text style={styles.detailLabel}>Recent Blockhash</Text>
            <Text style={styles.detailValue} numberOfLines={1} ellipsizeMode="middle">
              {transaction.transaction.message.recentBlockhash}
            </Text>
          </View>
        </Card.Content>
      </Card>

      {/* Instructions */}
      <Card style={styles.card}>
        <Card.Title 
          title="Instructions" 
          subtitle={`${instructions.length} instruction${instructions.length !== 1 ? 's' : ''}`} 
        />
        <Card.Content>
          {instructions.length === 0 ? (
            <Text style={styles.emptyText}>No instructions found</Text>
          ) : (
            instructions.map((instruction: any, index: number) => {
              // Get program ID from account keys
              const programId = accounts[instruction.programIndex];
              
              // Determine program name based on ID
              let programName = 'Unknown Program';
              if (programId === '11111111111111111111111111111111') {
                programName = 'System Program';
              } else if (programId === 'TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA') {
                programName = 'Token Program';
              }
              
              return (
                <View key={index} style={styles.instructionCard}>
                  <Text style={styles.instructionTitle}>
                    Instruction {index + 1}
                  </Text>
                  <Text style={styles.programName}>{programName}</Text>
                  
                  <Divider style={styles.divider} />
                  
                  <Text style={styles.accountsTitle}>Accounts:</Text>
                  {instruction.accounts.map((accountIdx: number, idx: number) => (
                    <Text key={idx} style={styles.accountText} numberOfLines={1}>
                      {idx + 1}. {accounts[accountIdx]}
                    </Text>
                  ))}
                  
                  {instruction.data && (
                    <>
                      <Text style={styles.dataTitle}>Data:</Text>
                      <Text style={styles.dataText} numberOfLines={3} ellipsizeMode="tail">
                        {instruction.data}
                      </Text>
                    </>
                  )}
                </View>
              );
            })
          )}
        </Card.Content>
      </Card>

      {/* Account Balances */}
      <Card style={styles.card}>
        <Card.Title title="Account Balances" />
        <Card.Content>
          {transaction.meta?.preBalances && transaction.meta?.postBalances ? (
            accounts.map((account: string, index: number) => {
              const preBalance = transaction.meta.preBalances[index] / 1_000_000_000;
              const postBalance = transaction.meta.postBalances[index] / 1_000_000_000;
              const change = postBalance - preBalance;
              const changeColor = change > 0 ? '#14F195' : change < 0 ? '#FF5C5C' : '#AAA';
              
              return (
                <View key={index} style={styles.balanceRow}>
                  <Text style={styles.accountAddress} numberOfLines={1} ellipsizeMode="middle">
                    {account}
                  </Text>
                  <View style={styles.balanceValues}>
                    <Text style={styles.balanceText}>
                      {postBalance.toFixed(9)} SOL
                    </Text>
                    {change !== 0 && (
                      <Text style={[styles.balanceChange, { color: changeColor }]}>
                        {change > 0 ? '+' : ''}{change.toFixed(9)}
                      </Text>
                    )}
                  </View>
                </View>
              );
            })
          ) : (
            <Text style={styles.emptyText}>No balance information available</Text>
          )}
        </Card.Content>
      </Card>

      {/* Log Messages (if available) */}
      {transaction.meta?.logMessages && transaction.meta.logMessages.length > 0 && (
        <Card style={styles.card}>
          <Card.Title title="Log Messages" />
          <Card.Content>
            {transaction.meta.logMessages.map((log: string, index: number) => (
              <Text key={index} style={styles.logMessage}>{log}</Text>
            ))}
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
    justifyContent: 'center',
    alignItems: 'center',
  },
  card: {
    marginBottom: 16,
    elevation: 4,
  },
  headerRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: '#FFF',
  },
  statusBadge: {
    paddingHorizontal: 12,
    paddingVertical: 4,
    borderRadius: 16,
    fontSize: 12,
    fontWeight: 'bold',
    color: '#000',
  },
  signatureLabel: {
    fontSize: 12,
    color: '#AAA',
    marginBottom: 4,
  },
  signatureText: {
    fontFamily: 'monospace',
    backgroundColor: '#1A1A1A',
    padding: 12,
    borderRadius: 6,
    color: '#FFF',
    marginBottom: 16,
  },
  explorerButton: {
    marginTop: 8,
  },
  detailRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderBottomColor: '#333',
  },
  detailLabel: {
    color: '#AAA',
    fontWeight: 'bold',
  },
  detailValue: {
    color: '#FFF',
    maxWidth: '60%',
  },
  instructionCard: {
    backgroundColor: '#1A1A1A',
    padding: 12,
    borderRadius: 8,
    marginBottom: 8,
  },
  instructionTitle: {
    fontWeight: 'bold',
    color: '#FFF',
    marginBottom: 4,
  },
  programName: {
    color: '#14F195',
    fontFamily: 'monospace',
    fontSize: 12,
  },
  divider: {
    backgroundColor: '#333',
    marginVertical: 8,
  },
  accountsTitle: {
    color: '#AAA',
    fontSize: 12,
    marginBottom: 4,
  },
  accountText: {
    color: '#CCC',
    fontFamily: 'monospace',
    fontSize: 11,
    marginBottom: 2,
  },
  dataTitle: {
    color: '#AAA',
    fontSize: 12,
    marginTop: 8,
    marginBottom: 4,
  },
  dataText: {
    color: '#CCC',
    fontFamily: 'monospace',
    fontSize: 11,
  },
  balanceRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    paddingVertical: 8,
    borderBottomWidth: 1,
    borderBottomColor: '#333',
  },
  accountAddress: {
    color: '#FFF',
    fontFamily: 'monospace',
    fontSize: 12,
    flex: 1,
    marginRight: 8,
  },
  balanceValues: {
    alignItems: 'flex-end',
  },
  balanceText: {
    color: '#FFF',
    fontFamily: 'monospace',
    fontSize: 12,
  },
  balanceChange: {
    fontFamily: 'monospace',
    fontSize: 11,
    marginTop: 2,
  },
  logMessage: {
    color: '#CCC',
    fontFamily: 'monospace',
    fontSize: 10,
    marginBottom: 4,
  },
  emptyText: {
    textAlign: 'center',
    color: '#AAA',
    padding: 16,
  },
});

export default TransactionDetailsScreen;