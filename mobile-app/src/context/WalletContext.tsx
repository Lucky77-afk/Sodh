import React, { createContext, useState, useContext, ReactNode } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { PublicKey } from '@solana/web3.js';

interface WalletContextType {
  publicKey: string | null;
  connectWallet: (publicKey: string) => Promise<void>;
  disconnectWallet: () => Promise<void>;
  isConnected: boolean;
}

const WalletContext = createContext<WalletContextType | undefined>(undefined);

export const WalletProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [publicKey, setPublicKey] = useState<string | null>(null);
  const [isConnected, setIsConnected] = useState<boolean>(false);

  // Load saved wallet on initialization
  React.useEffect(() => {
    const loadWallet = async () => {
      try {
        const savedPublicKey = await AsyncStorage.getItem('walletPublicKey');
        if (savedPublicKey) {
          setPublicKey(savedPublicKey);
          setIsConnected(true);
        }
      } catch (error) {
        console.error('Error loading wallet:', error);
      }
    };

    loadWallet();
  }, []);

  const connectWallet = async (publicKeyString: string) => {
    try {
      // Validate that the string is a valid public key
      new PublicKey(publicKeyString);
      
      // Save to state and storage
      setPublicKey(publicKeyString);
      await AsyncStorage.setItem('walletPublicKey', publicKeyString);
      setIsConnected(true);
    } catch (error) {
      console.error('Invalid public key:', error);
      throw new Error('Invalid public key format');
    }
  };

  const disconnectWallet = async () => {
    try {
      setPublicKey(null);
      await AsyncStorage.removeItem('walletPublicKey');
      setIsConnected(false);
    } catch (error) {
      console.error('Error disconnecting wallet:', error);
      throw error;
    }
  };

  return (
    <WalletContext.Provider value={{ publicKey, connectWallet, disconnectWallet, isConnected }}>
      {children}
    </WalletContext.Provider>
  );
};

export const useWallet = () => {
  const context = useContext(WalletContext);
  if (context === undefined) {
    throw new Error('useWallet must be used within a WalletProvider');
  }
  return context;
};