import React, { useState } from 'react';
import { View, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import { TextInput, Button, Card, Title, Paragraph, Divider, Chip } from 'react-native-paper';
import { useNavigation } from '@react-navigation/native';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import solanaService from '../services/solana-service';

const ExplorerScreen = () => {
  const navigation = useNavigation();
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [searchType, setSearchType] = useState<'account' | 'transaction'>('account');

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      setError('Please enter a valid search query');
      return;
    }

    setLoading(true);
    setError(null);
    
    try {
      if (searchType === 'account') {
        // Fetch account info and transactions
        const balance = await solanaService.getBalance(searchQuery);
        const transactions = await solanaService.getTransactionHistory(searchQuery);
        
        setSearchResults({
          type: 'account',
          address: searchQuery,
          balance,
          transactions: transactions.slice(0, 5) // Get first 5 transactions
        });
      } else {
        // Fetch transaction info
        const txInfo = await solanaService.getTransactionDetails(searchQuery);
        setSearchResults({
          type: 'transaction',
          signature: searchQuery,
          details: txInfo
        });
      }
    } catch (err) {
      console.error('Search error:', err);
      setError(`Invalid ${searchType}. Please check and try again.`);
    } finally {
      setLoading(false);
    }
  };

  const renderAccountResults = () => {
    const { address, balance, transactions } = searchResults;
    
    return (
      <Card style={styles.resultCard}>
        <Card.Content>
          <Title style={styles.title}>Account Information</Title>
          <View style={styles.infoRow}>
            <Paragraph style={styles.label}>Address:</Paragraph>
            <Paragraph style={styles.value} numberOfLines={1} ellipsizeMode="middle">
              {address}
            </Paragraph>
          </View>
          <View style={styles.infoRow}>
            <Paragraph style={styles.label}>Balance:</Paragraph>
            <Paragraph style={styles.value}>{balance} SOL</Paragraph>
          </View>
          
          <Divider style={styles.divider} />
          
          <Title style={styles.title}>Recent Transactions</Title>
          {transactions.length > 0 ? (
            transactions.map((tx, index) => (
              <TouchableOpacity
                key={index}
                onPress={() => navigation.navigate('TransactionDetail', { signature: tx.signature })}
              >
                <View style={styles.transactionItem}>
                  <Paragraph style={styles.transactionText} numberOfLines={1} ellipsizeMode="middle">
                    {tx.signature}
                  </Paragraph>
                  <MaterialCommunityIcons name="chevron-right" size={24} color="#BDBDBD" />
                </View>
                {index < transactions.length - 1 && <Divider style={styles.itemDivider} />}
              </TouchableOpacity>
            ))
          ) : (
            <Paragraph style={styles.noDataText}>No transactions found</Paragraph>
          )}
          
          {transactions.length > 0 && (
            <Button 
              mode="text" 
              onPress={() => {}} 
              style={styles.viewAllButton}
            >
              View All Transactions
            </Button>
          )}
        </Card.Content>
      </Card>
    );
  };

  const renderTransactionResults = () => {
    const { signature, details } = searchResults;
    
    if (!details) {
      return (
        <Card style={styles.resultCard}>
          <Card.Content>
            <Title style={styles.title}>Transaction Details</Title>
            <Paragraph style={styles.error}>Transaction not found</Paragraph>
          </Card.Content>
        </Card>
      );
    }
    
    return (
      <Card style={styles.resultCard}>
        <Card.Content>
          <Title style={styles.title}>Transaction Details</Title>
          <View style={styles.infoRow}>
            <Paragraph style={styles.label}>Signature:</Paragraph>
            <Paragraph style={styles.value} numberOfLines={1} ellipsizeMode="middle">
              {signature}
            </Paragraph>
          </View>
          <View style={styles.infoRow}>
            <Paragraph style={styles.label}>Slot:</Paragraph>
            <Paragraph style={styles.value}>{details.slot}</Paragraph>
          </View>
          <View style={styles.infoRow}>
            <Paragraph style={styles.label}>Block Time:</Paragraph>
            <Paragraph style={styles.value}>
              {details.blockTime ? new Date(details.blockTime * 1000).toLocaleString() : 'N/A'}
            </Paragraph>
          </View>
          <View style={styles.infoRow}>
            <Paragraph style={styles.label}>Status:</Paragraph>
            <Chip 
              style={[styles.statusChip, { backgroundColor: details.meta?.err ? '#F44336' : '#4CAF50' }]}
            >
              {details.meta?.err ? 'Failed' : 'Success'}
            </Chip>
          </View>
          
          <Button
            mode="contained"
            style={styles.button}
            onPress={() => navigation.navigate('TransactionDetail', { signature })}
          >
            View Full Details
          </Button>
        </Card.Content>
      </Card>
    );
  };

  return (
    <ScrollView style={styles.container}>
      <Card style={styles.searchCard}>
        <Card.Content>
          <Title style={styles.title}>Solana Explorer</Title>
          
          <View style={styles.searchTypeContainer}>
            <TouchableOpacity
              style={[
                styles.searchTypeButton,
                searchType === 'account' && styles.activeSearchType
              ]}
              onPress={() => setSearchType('account')}
            >
              <Paragraph style={[
                styles.searchTypeText,
                searchType === 'account' && styles.activeSearchTypeText
              ]}>
                Account
              </Paragraph>
            </TouchableOpacity>
            <TouchableOpacity
              style={[
                styles.searchTypeButton,
                searchType === 'transaction' && styles.activeSearchType
              ]}
              onPress={() => setSearchType('transaction')}
            >
              <Paragraph style={[
                styles.searchTypeText,
                searchType === 'transaction' && styles.activeSearchTypeText
              ]}>
                Transaction
              </Paragraph>
            </TouchableOpacity>
          </View>
          
          <TextInput
            label={`Enter ${searchType} address`}
            value={searchQuery}
            onChangeText={setSearchQuery}
            style={styles.searchInput}
            theme={{ colors: { primary: '#512DA8' } }}
          />
          
          {error && <Paragraph style={styles.error}>{error}</Paragraph>}
          
          <Button
            mode="contained"
            onPress={handleSearch}
            loading={loading}
            disabled={loading}
            style={styles.button}
          >
            Search
          </Button>
        </Card.Content>
      </Card>

      {searchResults && (
        searchResults.type === 'account' ? renderAccountResults() : renderTransactionResults()
      )}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1E1E1E',
    padding: 16,
  },
  searchCard: {
    marginBottom: 16,
    backgroundColor: '#2C2C2C',
    borderRadius: 8,
  },
  resultCard: {
    backgroundColor: '#2C2C2C',
    borderRadius: 8,
    marginBottom: 16,
  },
  title: {
    color: '#FFFFFF',
    marginBottom: 12,
  },
  searchTypeContainer: {
    flexDirection: 'row',
    marginBottom: 16,
  },
  searchTypeButton: {
    flex: 1,
    paddingVertical: 8,
    alignItems: 'center',
    borderBottomWidth: 2,
    borderBottomColor: 'transparent',
  },
  activeSearchType: {
    borderBottomColor: '#512DA8',
  },
  searchTypeText: {
    color: '#BDBDBD',
  },
  activeSearchTypeText: {
    color: '#FFFFFF',
  },
  searchInput: {
    backgroundColor: '#3C3C3C',
    marginBottom: 12,
  },
  button: {
    marginTop: 12,
    backgroundColor: '#512DA8',
  },
  viewAllButton: {
    marginTop: 8,
    alignSelf: 'center',
  },
  error: {
    color: '#F44336',
    marginTop: 8,
  },
  infoRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  label: {
    color: '#BDBDBD',
    flex: 1,
  },
  value: {
    color: '#E0E0E0',
    flex: 2,
    textAlign: 'right',
  },
  divider: {
    backgroundColor: '#424242',
    height: 1,
    marginVertical: 16,
  },
  itemDivider: {
    backgroundColor: '#424242',
    height: 1,
    marginVertical: 8,
  },
  transactionItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 8,
  },
  transactionText: {
    color: '#E0E0E0',
    flex: 1,
  },
  noDataText: {
    color: '#BDBDBD',
    fontStyle: 'italic',
    textAlign: 'center',
    marginVertical: 8,
  },
  statusChip: {
    height: 24,
    justifyContent: 'center',
  },
});

export default ExplorerScreen; 