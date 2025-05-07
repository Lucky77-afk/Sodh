import React, { useState } from 'react';
import { View, StyleSheet, ScrollView, KeyboardAvoidingView, Platform } from 'react-native';
import { Card, Title, Paragraph, TextInput, Button, HelperText } from 'react-native-paper';
import { useNavigation } from '@react-navigation/native';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { PublicKey } from '@solana/web3.js';

import { useWallet } from '../context/WalletContext';
import { NavigationProp } from '../types/components';

const ConnectWalletScreen = () => {
  const navigation = useNavigation<NavigationProp>();
  const { connectWallet } = useWallet();
  
  const [publicKey, setPublicKey] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  const handleConnect = async () => {
    if (!publicKey.trim()) {
      setError('Please enter a public key');
      return;
    }

    try {
      setError(null);
      setLoading(true);
      
      // Validate the public key format
      new PublicKey(publicKey.trim());
      
      // Connect the wallet
      await connectWallet(publicKey.trim());
      navigation.goBack();
    } catch (err) {
      console.error('Error connecting wallet:', err);
      setError('Invalid public key format');
    } finally {
      setLoading(false);
    }
  };

  return (
    <KeyboardAvoidingView 
      style={styles.container}
      behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
    >
      <ScrollView contentContainerStyle={styles.scrollContent}>
        <Card style={styles.card}>
          <Card.Content>
            <View style={styles.header}>
              <MaterialCommunityIcons 
                name="wallet-outline" 
                size={48} 
                color="#512DA8" 
                style={styles.icon}
              />
              <Title style={styles.title}>Connect Wallet</Title>
              <Paragraph style={styles.paragraph}>
                Enter your Solana wallet public key to view your balances and transactions
              </Paragraph>
            </View>

            <TextInput
              label="Public Key"
              value={publicKey}
              onChangeText={setPublicKey}
              mode="outlined"
              style={styles.input}
              autoCapitalize="none"
              autoCorrect={false}
              placeholder="Enter your wallet public key"
              error={!!error}
              disabled={loading}
            />
            
            {error && (
              <HelperText type="error" visible={!!error}>
                {error}
              </HelperText>
            )}

            <Button
              mode="contained"
              onPress={handleConnect}
              style={styles.button}
              loading={loading}
              disabled={loading}
            >
              Connect Wallet
            </Button>

            <Button
              mode="text"
              onPress={() => navigation.goBack()}
              style={styles.cancelButton}
              disabled={loading}
            >
              Cancel
            </Button>
          </Card.Content>
        </Card>

        <Card style={styles.infoCard}>
          <Card.Content>
            <Title style={styles.infoTitle}>About View-Only Wallets</Title>
            <Paragraph style={styles.infoText}>
              This is a view-only wallet connection. You can:
            </Paragraph>
            <View style={styles.featureList}>
              <View style={styles.featureItem}>
                <MaterialCommunityIcons name="eye" size={20} color="#4CAF50" />
                <Paragraph style={styles.featureText}>View your SOL balance</Paragraph>
              </View>
              <View style={styles.featureItem}>
                <MaterialCommunityIcons name="history" size={20} color="#4CAF50" />
                <Paragraph style={styles.featureText}>Check transaction history</Paragraph>
              </View>
              <View style={styles.featureItem}>
                <MaterialCommunityIcons name="shield-check" size={20} color="#4CAF50" />
                <Paragraph style={styles.featureText}>No private keys required</Paragraph>
              </View>
            </View>
          </Card.Content>
        </Card>
      </ScrollView>
    </KeyboardAvoidingView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1E1E1E',
  },
  scrollContent: {
    padding: 16,
  },
  card: {
    backgroundColor: '#2C2C2C',
    borderRadius: 8,
    marginBottom: 16,
  },
  header: {
    alignItems: 'center',
    marginBottom: 24,
  },
  icon: {
    marginBottom: 16,
  },
  title: {
    color: '#FFFFFF',
    marginBottom: 8,
    textAlign: 'center',
  },
  paragraph: {
    color: '#E0E0E0',
    textAlign: 'center',
    marginBottom: 8,
  },
  input: {
    marginBottom: 8,
    backgroundColor: '#3C3C3C',
  },
  button: {
    marginTop: 16,
    backgroundColor: '#512DA8',
  },
  cancelButton: {
    marginTop: 8,
  },
  infoCard: {
    backgroundColor: '#2C2C2C',
    borderRadius: 8,
  },
  infoTitle: {
    color: '#FFFFFF',
    marginBottom: 12,
  },
  infoText: {
    color: '#E0E0E0',
    marginBottom: 16,
  },
  featureList: {
    marginTop: 8,
  },
  featureItem: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 12,
  },
  featureText: {
    color: '#E0E0E0',
    marginLeft: 12,
  },
});

 