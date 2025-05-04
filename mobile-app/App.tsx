import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { StatusBar } from 'expo-status-bar';
import { Provider as PaperProvider, DefaultTheme } from 'react-native-paper';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import AppNavigator from './src/navigation/AppNavigator';
import { UniversalWalletProvider } from './src/context/UniversalWalletProvider';

// Define custom theme for Solana aesthetics
const theme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    primary: '#14F195', // Solana green
    accent: '#9945FF', // Solana purple
    background: '#131313', // Dark background
    surface: '#1E1E1E', // Card background
    text: '#FFFFFF',
    error: '#FF5C5C',
    notification: '#14F195',
  },
  dark: true,
};

export default function App() {
  return (
    <SafeAreaProvider>
      <PaperProvider theme={theme}>
        <UniversalWalletProvider>
          <NavigationContainer theme={{
            dark: true,
            colors: {
              primary: '#14F195',
              background: '#131313', 
              card: '#1E1E1E',
              text: '#FFFFFF',
              border: '#333333',
              notification: '#9945FF',
            }
          }}>
            <StatusBar style="light" />
            <AppNavigator />
          </NavigationContainer>
        </UniversalWalletProvider>
      </PaperProvider>
    </SafeAreaProvider>
  );
}