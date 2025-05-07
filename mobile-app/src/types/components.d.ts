import { NativeStackNavigationProp } from '@react-navigation/native-stack';

export type RootStackParamList = {
  Home: undefined;
  Explorer: undefined;
  Wallet: undefined;
  Settings: undefined;
  ConnectWallet: undefined;
  TransactionDetail: { signature: string };
  TransactionHistory: { address: string };
};

export type NavigationProp = NativeStackNavigationProp<RootStackParamList>;

export interface Transaction {
  signature: string;
  slot: number;
  blockTime: number;
  status: 'success' | 'error';
  fee: number;
  amount?: number;
  type?: string;
}

export interface WalletState {
  publicKey: string | null;
  isConnected: boolean;
}

export interface WalletContextType extends WalletState {
  connectWallet: (publicKey: string) => Promise<void>;
  disconnectWallet: () => Promise<void>;
} 