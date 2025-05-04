import React, { createContext, useState, useContext, useEffect } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Connection, PublicKey, clusterApiUrl } from '@solana/web3.js';

// Define types
type WalletContextType = {
  connected: boolean;
  walletAddress: string | null;
  balance: number;
  connectWallet: (address: string) => Promise<void>;
  disconnectWallet: () => Promise<void>;
  getBalance: () => Promise<void>;
  connection: Connection | null;
};

// Create context with default values
const WalletContext = createContext<WalletContextType>({
  connected: false,
  walletAddress: null,
  balance: 0,
  connectWallet: async () => {},
  disconnectWallet: async () => {},
  getBalance: async () => {},
  connection: null,
});

// Create provider component
export const WalletProvider: React.FC<{children: React.ReactNode}> = ({ children }) => {
  const [connected, setConnected] = useState(false);
  const [walletAddress, setWalletAddress] = useState<string | null>(null);
  const [balance, setBalance] = useState(0);
  const [connection, setConnection] = useState<Connection | null>(null);

  // Initialize Solana connection
  useEffect(() => {
    // Connect to Solana devnet
    const conn = new Connection(clusterApiUrl('devnet'));
    setConnection(conn);

    // Check if wallet was previously connected
    const checkStoredWallet = async () => {
      try {
        const storedAddress = await AsyncStorage.getItem('walletAddress');
        if (storedAddress) {
          setWalletAddress(storedAddress);
          setConnected(true);
        }
      } catch (error) {
        console.error('Error loading wallet from storage:', error);
      }
    };

    checkStoredWallet();
  }, []);

  // Get wallet balance whenever the wallet address changes
  useEffect(() => {
    if (connected && walletAddress && connection) {
      getBalance();
    }
  }, [connected, walletAddress, connection]);

  // Connect to wallet by storing the address
  const connectWallet = async (address: string) => {
    try {
      // Validate address format
      new PublicKey(address);
      
      setWalletAddress(address);
      setConnected(true);
      
      // Store wallet address for persistence
      await AsyncStorage.setItem('walletAddress', address);
      
      // Get initial balance
      await getBalance();
    } catch (error) {
      console.error('Error connecting wallet:', error);
      throw new Error('Invalid wallet address format');
    }
  };

  // Disconnect wallet
  const disconnectWallet = async () => {
    try {
      setWalletAddress(null);
      setConnected(false);
      setBalance(0);
      await AsyncStorage.removeItem('walletAddress');
    } catch (error) {
      console.error('Error disconnecting wallet:', error);
    }
  };

  // Get SOL balance
  const getBalance = async () => {
    if (!connection || !walletAddress) {
      return;
    }

    try {
      const publicKey = new PublicKey(walletAddress);
      const bal = await connection.getBalance(publicKey);
      
      // Convert lamports to SOL (1 SOL = 1,000,000,000 lamports)
      setBalance(bal / 1000000000);
    } catch (error) {
      console.error('Error fetching balance:', error);
    }
  };

  return (
    <WalletContext.Provider
      value={{
        connected,
        walletAddress,
        balance,
        connectWallet,
        disconnectWallet,
        getBalance,
        connection,
      }}
    >
      {children}
    </WalletContext.Provider>
  );
};

// Custom hook to use the wallet context
export const useWallet = () => useContext(WalletContext);