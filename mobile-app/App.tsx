import React from 'react';
import { StatusBar } from 'expo-status-bar';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { 
  Provider as PaperProvider, 
  DefaultTheme as PaperDefaultTheme
} from 'react-native-paper';
import AppNavigator from './src/navigation/AppNavigator';
import { WalletProvider } from './src/context/WalletContext';

// Create custom theme with Solana colors
const theme = {
  ...PaperDefaultTheme,
  colors: {
    ...PaperDefaultTheme.colors,
    primary: '#14F195', // Solana green
    accent: '#9945FF',  // Solana purple
    background: '#131313',
    surface: '#1E1E1E',
    text: '#FFFFFF',
    error: '#FF5C5C',
  },
  dark: true,
};

export default function App() {
  return (
    <SafeAreaProvider>
      <PaperProvider theme={theme}>
        <WalletProvider>
          <StatusBar style="light" />
          <AppNavigator />
        </WalletProvider>
      </PaperProvider>
    </SafeAreaProvider>
  );
}