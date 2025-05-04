import React, { createContext, useContext, useState, useEffect } from 'react';
import { Alert, Linking } from 'react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import * as Clipboard from 'expo-clipboard';
import { Connection, PublicKey, LAMPORTS_PER_SOL } from '@solana/web3.js';
import { getAccountInfo } from '../services/solana-service';

// Supported wallet types
export enum WalletType {
  PHANTOM = 'phantom',
  SOLFLARE = 'solflare',
  SOLLET = 'sollet',
  SLOPE = 'slope',
  TRUSTWALLET = 'trustwallet',
  CUSTOM = 'custom'
}

interface WalletContextType {
  address: string | null;
  balance: number;
  connected: boolean;
  walletType: WalletType | null;
  connectWallet: (address: string, type?: WalletType) => Promise<void>;
  disconnectWallet: () => Promise<void>;
  openWalletApp: () => Promise<void>;
  refreshBalance: () => Promise<void>;
  deepLinkConnect: () => Promise<void>;
  pasteFromClipboard: () => Promise<string>;
}

const WalletContext = createContext<WalletContextType>({
  address: null,
  balance: 0,
  connected: false,
  walletType: null,
  connectWallet: async () => {},
  disconnectWallet: async () => {},
  openWalletApp: async () => {},
  refreshBalance: async () => {},
  deepLinkConnect: async () => {},
  pasteFromClipboard: async () => '',
});

export const UniversalWalletProvider: React.FC<{children: React.ReactNode}> = ({ children }) => {
  const [address, setAddress] = useState<string | null>(null);
  const [balance, setBalance] = useState<number>(0);
  const [walletType, setWalletType] = useState<WalletType | null>(null);
  const [connection, setConnection] = useState<Connection | null>(null);
  const [isRefreshing, setIsRefreshing] = useState<boolean>(false);
  
  // Initialize Solana connection
  useEffect(() => {
    const conn = new Connection('https://api.devnet.solana.com');
    setConnection(conn);
  }, []);
  
  // Load wallet from storage on start
  useEffect(() => {
    const loadWallet = async () => {
      try {
        const storedAddress = await AsyncStorage.getItem('walletAddress');
        const storedType = await AsyncStorage.getItem('walletType');
        
        if (storedAddress) {
          setAddress(storedAddress);
          setWalletType(storedType as WalletType || WalletType.CUSTOM);
          await loadBalance(storedAddress);
        }
      } catch (error) {
        console.error('Error loading wallet', error);
      }
    };
    
    loadWallet();
  }, []);
  
  // Load balance for an address
  const loadBalance = async (walletAddress: string) => {
    if (!connection || !walletAddress) return;
    
    try {
      setIsRefreshing(true);
      const accountInfo = await getAccountInfo(connection, walletAddress);
      
      if (accountInfo && accountInfo.result) {
        setBalance(accountInfo.result.balance_sol);
      } else {
        // If API call fails, try direct balance check
        try {
          const pubkey = new PublicKey(walletAddress);
          const balance = await connection.getBalance(pubkey);
          setBalance(balance / LAMPORTS_PER_SOL);
        } catch (error) {
          console.error('Direct balance check failed', error);
          setBalance(0);
        }
      }
    } catch (error) {
      console.error('Error loading balance', error);
      setBalance(0);
    } finally {
      setIsRefreshing(false);
    }
  };
  
  // Connect to a wallet
  const connectWallet = async (walletAddress: string, type: WalletType = WalletType.CUSTOM) => {
    try {
      // Validate Solana address format (basic check)
      if (!walletAddress || walletAddress.length < 32) {
        Alert.alert('Invalid Address', 'Please enter a valid Solana wallet address');
        return;
      }
      
      // Try to create a PublicKey object to verify format
      try {
        new PublicKey(walletAddress);
      } catch (e) {
        Alert.alert('Invalid Address', 'The address format is not valid for Solana');
        return;
      }
      
      // Set state
      setAddress(walletAddress);
      setWalletType(type);
      
      // Save to storage
      await AsyncStorage.setItem('walletAddress', walletAddress);
      await AsyncStorage.setItem('walletType', type);
      
      // Load balance
      await loadBalance(walletAddress);
      
      console.log(`Connected to wallet: ${walletAddress} (${type})`);
    } catch (error) {
      console.error('Error connecting wallet', error);
      Alert.alert('Connection Error', 'Could not connect to wallet');
    }
  };
  
  // Disconnect wallet
  const disconnectWallet = async () => {
    try {
      setAddress(null);
      setBalance(0);
      setWalletType(null);
      
      // Clear from storage
      await AsyncStorage.removeItem('walletAddress');
      await AsyncStorage.removeItem('walletType');
      
      console.log('Disconnected wallet');
    } catch (error) {
      console.error('Error disconnecting wallet', error);
    }
  };
  
  // Open the wallet app
  const openWalletApp = async () => {
    if (!walletType) {
      Alert.alert('No Wallet Selected', 'Please connect a wallet first');
      return;
    }
    
    let url = '';
    
    switch (walletType) {
      case WalletType.PHANTOM:
        url = 'https://phantom.app/ul/browse';
        break;
      case WalletType.SOLFLARE:
        url = 'https://solflare.com';
        break;
      case WalletType.SLOPE:
        url = 'https://slope.finance';
        break;
      case WalletType.TRUSTWALLET:
        url = 'https://trustwallet.com';
        break;
      default:
        Alert.alert('Cannot Open Wallet', 'No deep link available for this wallet type');
        return;
    }
    
    try {
      const supported = await Linking.canOpenURL(url);
      
      if (supported) {
        await Linking.openURL(url);
      } else {
        Alert.alert(
          'Wallet App Not Installed',
          `The ${walletType} app is not installed. Would you like to download it?`,
          [
            { text: 'Cancel', style: 'cancel' },
            { text: 'Download', onPress: () => Linking.openURL(`https://www.google.com/search?q=${walletType}+wallet+download`) }
          ]
        );
      }
    } catch (error) {
      console.error('Error opening wallet app', error);
      Alert.alert('Error', 'Could not open wallet app');
    }
  };
  
  // Refresh balance
  const refreshBalance = async () => {
    if (address) {
      await loadBalance(address);
    }
  };
  
  // Deep link connect for mobile wallets
  const deepLinkConnect = async () => {
    try {
      // This would normally use WalletConnect or a similar protocol
      // For now, we'll just show an educational message since we're in view-only mode
      Alert.alert(
        'Wallet Connection',
        'In a production app, this would open your wallet app for secure connection. For this demo, please paste your wallet address manually.',
        [
          { text: 'Cancel', style: 'cancel' },
          { 
            text: 'Choose Wallet', 
            onPress: () => {
              Alert.alert(
                'Select Wallet',
                'Which wallet would you like to use?',
                [
                  { text: 'Phantom', onPress: () => setWalletType(WalletType.PHANTOM) },
                  { text: 'Solflare', onPress: () => setWalletType(WalletType.SOLFLARE) },
                  { text: 'Trust Wallet', onPress: () => setWalletType(WalletType.TRUSTWALLET) },
                  { text: 'Other', onPress: () => setWalletType(WalletType.CUSTOM) },
                ]
              );
            }
          }
        ]
      );
    } catch (error) {
      console.error('Deep link error', error);
    }
  };
  
  // Helper to paste from clipboard
  const pasteFromClipboard = async (): Promise<string> => {
    try {
      const text = await Clipboard.getStringAsync();
      return text || '';
    } catch (error) {
      console.error('Clipboard error', error);
      return '';
    }
  };
  
  return (
    <WalletContext.Provider
      value={{
        address,
        balance,
        connected: !!address,
        walletType,
        connectWallet,
        disconnectWallet,
        openWalletApp,
        refreshBalance,
        deepLinkConnect,
        pasteFromClipboard
      }}
    >
      {children}
    </WalletContext.Provider>
  );
};

export const useUniversalWallet = () => useContext(WalletContext);