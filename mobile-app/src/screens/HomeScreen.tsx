import React, { useState, useEffect } from 'react';
import { View, StyleSheet, ScrollView } from 'react-native';
import { Card, Title, Paragraph, Button, ActivityIndicator } from 'react-native-paper';
import { useNavigation } from '@react-navigation/native';
import solanaService from '../services/solana-service';
import { useWallet } from '../context/WalletContext';

const HomeScreen = () => {
  const navigation = useNavigation();
  const { publicKey, isConnected } = useWallet();
  const [networkStatus, setNetworkStatus] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchNetworkStatus = async () => {
      try {
        setLoading(true);
        const status = await solanaService.getNetworkStatus();
        setNetworkStatus(status);
        setError(null);
      } catch (err) {
        setError('Failed to fetch network status');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchNetworkStatus();
    // Refresh every 30 seconds
    const interval = setInterval(fetchNetworkStatus, 30000);
    return () => clearInterval(interval);
  }, []);

  const handleConnectWallet = () => {
    navigation.navigate('ConnectWallet');
  };

  return (
    <ScrollView style={styles.container}>
      {/* Network Status Card */}
      <Card style={styles.card}>
        <Card.Content>
          <Title style={styles.title}>Solana Network Status</Title>
          {loading ? (
            <ActivityIndicator size="small" color="#512DA8" />
          ) : error ? (
            <Paragraph style={styles.error}>{error}</Paragraph>
          ) : (
            <>
              <View style={styles.infoRow}>
                <Paragraph style={styles.label}>Network:</Paragraph>
                <Paragraph style={styles.value}>Devnet</Paragraph>
              </View>
              <View style={styles.infoRow}>
                <Paragraph style={styles.label}>Current Slot:</Paragraph>
                <Paragraph style={styles.value}>{networkStatus?.slot}</Paragraph>
              </View>
              <View style={styles.infoRow}>
                <Paragraph style={styles.label}>Version:</Paragraph>
                <Paragraph style={styles.value}>{networkStatus?.version?.['solana-core']}</Paragraph>
              </View>
            </>
          )}
        </Card.Content>
      </Card>

      {/* Wallet Card */}
      <Card style={styles.card}>
        <Card.Content>
          <Title style={styles.title}>Wallet</Title>
          {isConnected ? (
            <>
              <View style={styles.infoRow}>
                <Paragraph style={styles.label}>Public Key:</Paragraph>
                <Paragraph style={styles.value} numberOfLines={1} ellipsizeMode="middle">
                  {publicKey}
                </Paragraph>
              </View>
              <Button
                mode="contained"
                style={styles.button}
                onPress={() => navigation.navigate('Wallet')}
              >
                View Wallet
              </Button>
            </>
          ) : (
            <>
              <Paragraph style={styles.paragraph}>
                Connect a wallet to view your SOL and tokens.
              </Paragraph>
              <Button mode="contained" style={styles.button} onPress={handleConnectWallet}>
                Connect Wallet
              </Button>
            </>
          )}
        </Card.Content>
      </Card>

      {/* Features Card */}
      <Card style={styles.card}>
        <Card.Content>
          <Title style={styles.title}>Explorer Features</Title>
          <Paragraph style={styles.paragraph}>
            • View real-time blockchain data
          </Paragraph>
          <Paragraph style={styles.paragraph}>
            • Track transaction history
          </Paragraph>
          <Paragraph style={styles.paragraph}>
            • Interact with smart contracts
          </Paragraph>
          <Paragraph style={styles.paragraph}>
            • Manage projects and collaborations
          </Paragraph>
          <Button
            mode="contained"
            style={styles.button}
            onPress={() => navigation.navigate('Explorer')}
          >
            Open Explorer
          </Button>
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
  title: {
    color: '#FFFFFF',
    marginBottom: 12,
  },
  paragraph: {
    color: '#E0E0E0',
    marginBottom: 8,
  },
  infoRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
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
  button: {
    marginTop: 12,
    backgroundColor: '#512DA8',
  },
  error: {
    color: '#F44336',
  },
});

export default HomeScreen; 