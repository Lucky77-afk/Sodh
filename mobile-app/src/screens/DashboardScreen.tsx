import React, { useState, useEffect } from 'react';
import { View, StyleSheet, ScrollView, ActivityIndicator, RefreshControl } from 'react-native';
import { Text, Card, useTheme, Button } from 'react-native-paper';
import { useWallet } from '../context/WalletContext';
import { Connection, clusterApiUrl } from '@solana/web3.js';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';

// Solana API service
import { getRecentBlocks, getRecentTransactions } from '../services/solana-service';

const DashboardScreen = () => {
  const theme = useTheme();
  const { connected } = useWallet();
  const [isLoading, setIsLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [networkStatus, setNetworkStatus] = useState<any>({});
  const [recentBlocks, setRecentBlocks] = useState<any[]>([]);
  const [recentTransactions, setRecentTransactions] = useState<any[]>([]);
  const [error, setError] = useState<string | null>(null);

  // Initial data loading
  useEffect(() => {
    loadDashboardData();
  }, []);

  // Reload dashboard data
  const loadDashboardData = async () => {
    setIsLoading(true);
    setError(null);
    
    try {
      // Create a Solana connection to devnet
      const connection = new Connection(clusterApiUrl('devnet'));
      
      // Get network status
      const version = await connection.getVersion();
      const slot = await connection.getSlot();
      const blockTime = await connection.getBlockTime(slot);
      
      setNetworkStatus({
        version: version['solana-core'],
        slot,
        blockTime: blockTime ? new Date(blockTime * 1000).toLocaleString() : 'Unknown',
      });
      
      // Load recent blocks
      const blocks = await getRecentBlocks(connection, 5);
      setRecentBlocks(blocks);
      
      // Load recent transactions
      const txs = await getRecentTransactions(connection, 5);
      setRecentTransactions(txs);
      
    } catch (err) {
      console.error('Error loading dashboard data:', err);
      setError('Failed to load blockchain data. Please try again.');
    } finally {
      setIsLoading(false);
      setRefreshing(false);
    }
  };

  // Handle refresh
  const onRefresh = () => {
    setRefreshing(true);
    loadDashboardData();
  };

  if (isLoading && !refreshing) {
    return (
      <View style={[styles.container, styles.centered]}>
        <ActivityIndicator size="large" color={theme.colors.primary} />
        <Text style={{ color: theme.colors.text, marginTop: 16 }}>Loading blockchain data...</Text>
      </View>
    );
  }

  return (
    <ScrollView 
      style={[styles.container, { backgroundColor: theme.colors.background }]}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} />
      }
    >
      {/* Network Status */}
      <Card style={styles.card}>
        <Card.Title title="Solana Network Status" />
        <Card.Content>
          {error ? (
            <Text style={{ color: theme.colors.error }}>{error}</Text>
          ) : (
            <View>
              <View style={styles.statRow}>
                <Text style={styles.statLabel}>Network:</Text>
                <Text style={[styles.statValue, { color: theme.colors.primary }]}>Devnet</Text>
              </View>
              <View style={styles.statRow}>
                <Text style={styles.statLabel}>Version:</Text>
                <Text style={styles.statValue}>{networkStatus.version || 'Unknown'}</Text>
              </View>
              <View style={styles.statRow}>
                <Text style={styles.statLabel}>Current Slot:</Text>
                <Text style={styles.statValue}>{networkStatus.slot || 'Unknown'}</Text>
              </View>
              <View style={styles.statRow}>
                <Text style={styles.statLabel}>Block Time:</Text>
                <Text style={styles.statValue}>{networkStatus.blockTime || 'Unknown'}</Text>
              </View>
            </View>
          )}
        </Card.Content>
      </Card>

      {/* Recent Blocks */}
      <Card style={styles.card}>
        <Card.Title 
          title="Recent Blocks" 
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
          {recentBlocks.length === 0 ? (
            <Text>No recent blocks available</Text>
          ) : (
            recentBlocks.map((block, index) => (
              <Card key={index} style={styles.itemCard}>
                <View style={styles.blockItem}>
                  <Icon name="cube-outline" size={24} color={theme.colors.primary} />
                  <View style={styles.blockInfo}>
                    <Text style={styles.blockSlot}>Slot: {block.slot}</Text>
                    <Text style={styles.blockHash}>{block.blockhash?.substring(0, 15)}...</Text>
                    <Text style={styles.blockTime}>
                      {new Date(block.timestamp * 1000).toLocaleString()}
                    </Text>
                  </View>
                </View>
              </Card>
            ))
          )}
        </Card.Content>
      </Card>

      {/* Recent Transactions */}
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
          {recentTransactions.length === 0 ? (
            <Text>No recent transactions available</Text>
          ) : (
            recentTransactions.map((tx, index) => (
              <Card key={index} style={styles.itemCard}>
                <View style={styles.txItem}>
                  <Icon 
                    name={tx.status === 'Success' ? 'check-circle-outline' : 'alert-circle-outline'} 
                    size={24} 
                    color={tx.status === 'Success' ? theme.colors.primary : theme.colors.error} 
                  />
                  <View style={styles.txInfo}>
                    <Text style={styles.txSignature}>{tx.signature.substring(0, 15)}...</Text>
                    <View style={styles.txDetails}>
                      <Text style={styles.txType}>{tx.type}</Text>
                      <Text style={styles.txStatus}>{tx.status}</Text>
                    </View>
                    <Text style={styles.txTime}>{tx.block_time}</Text>
                  </View>
                </View>
              </Card>
            ))
          )}
        </Card.Content>
      </Card>

      {/* Wallet Connection Prompt */}
      {!connected && (
        <Card style={[styles.card, styles.walletPrompt]}>
          <Card.Content>
            <View style={styles.walletPromptContent}>
              <Icon name="wallet-outline" size={40} color={theme.colors.primary} />
              <Text style={styles.walletPromptText}>
                Connect a wallet to explore your Solana assets and transactions
              </Text>
              <Button 
                mode="contained" 
                onPress={() => {}} // Will navigate to Account screen
                style={styles.walletButton}
              >
                Connect Wallet
              </Button>
            </View>
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
  statRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 8,
  },
  statLabel: {
    fontWeight: 'bold',
    color: '#AAA',
  },
  statValue: {
    color: '#FFF',
  },
  itemCard: {
    marginBottom: 8,
    padding: 8,
  },
  blockItem: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  blockInfo: {
    marginLeft: 12,
    flex: 1,
  },
  blockSlot: {
    fontWeight: 'bold',
    color: '#FFF',
  },
  blockHash: {
    fontFamily: 'monospace',
    color: '#CCC',
  },
  blockTime: {
    fontSize: 12,
    color: '#AAA',
  },
  txItem: {
    flexDirection: 'row',
    alignItems: 'center',
  },
  txInfo: {
    marginLeft: 12,
    flex: 1,
  },
  txSignature: {
    fontFamily: 'monospace',
    fontWeight: 'bold',
    color: '#FFF',
  },
  txDetails: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginTop: 4,
  },
  txType: {
    color: '#CCC',
  },
  txStatus: {
    color: '#AAA',
  },
  txTime: {
    fontSize: 12,
    color: '#AAA',
  },
  walletPrompt: {
    backgroundColor: 'rgba(20, 241, 149, 0.1)',
    borderLeftWidth: 3,
    borderLeftColor: '#14F195',
  },
  walletPromptContent: {
    alignItems: 'center',
    padding: 16,
  },
  walletPromptText: {
    textAlign: 'center',
    marginVertical: 16,
    color: '#FFF',
  },
  walletButton: {
    marginTop: 8,
  },
});

export default DashboardScreen;