import React from 'react';
import { render, act } from '@testing-library/react-native';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { WalletProvider, useWallet } from '../WalletContext';
import { PublicKey } from '@solana/web3.js';

// Mock AsyncStorage
jest.mock('@react-native-async-storage/async-storage', () =>
  require('@react-native-async-storage/async-storage/jest/async-storage-mock')
);

// Mock @solana/web3.js
jest.mock('@solana/web3.js', () => ({
  PublicKey: jest.fn(),
}));

describe('WalletContext', () => {
  const TestComponent = () => {
    const wallet = useWallet();
    return (
      <>
        <Text testID="publicKey">{wallet.publicKey || 'no-key'}</Text>
        <Text testID="isConnected">{wallet.isConnected.toString()}</Text>
        <Button
          testID="connect"
          onPress={() => wallet.connectWallet('test-key')}
          title="Connect"
        />
        <Button
          testID="disconnect"
          onPress={() => wallet.disconnectWallet()}
          title="Disconnect"
        />
      </>
    );
  };

  beforeEach(() => {
    jest.clearAllMocks();
    AsyncStorage.clear();
  });

  it('provides initial state', () => {
    const { getByTestId } = render(
      <WalletProvider>
        <TestComponent />
      </WalletProvider>
    );

    expect(getByTestId('publicKey').props.children).toBe('no-key');
    expect(getByTestId('isConnected').props.children).toBe('false');
  });

  it('loads saved wallet on mount', async () => {
    const savedPublicKey = 'saved-key';
    await AsyncStorage.setItem('wallet_public_key', savedPublicKey);

    const { getByTestId } = render(
      <WalletProvider>
        <TestComponent />
      </WalletProvider>
    );

    await act(async () => {
      await new Promise(resolve => setTimeout(resolve, 0));
    });

    expect(getByTestId('publicKey').props.children).toBe(savedPublicKey);
    expect(getByTestId('isConnected').props.children).toBe('true');
  });

  it('connects wallet', async () => {
    const { getByTestId } = render(
      <WalletProvider>
        <TestComponent />
      </WalletProvider>
    );

    await act(async () => {
      fireEvent.press(getByTestId('connect'));
    });

    expect(getByTestId('publicKey').props.children).toBe('test-key');
    expect(getByTestId('isConnected').props.children).toBe('true');
    expect(AsyncStorage.setItem).toHaveBeenCalledWith('wallet_public_key', 'test-key');
  });

  it('disconnects wallet', async () => {
    // First connect a wallet
    await AsyncStorage.setItem('wallet_public_key', 'test-key');

    const { getByTestId } = render(
      <WalletProvider>
        <TestComponent />
      </WalletProvider>
    );

    await act(async () => {
      fireEvent.press(getByTestId('disconnect'));
    });

    expect(getByTestId('publicKey').props.children).toBe('no-key');
    expect(getByTestId('isConnected').props.children).toBe('false');
    expect(AsyncStorage.removeItem).toHaveBeenCalledWith('wallet_public_key');
  });

  it('validates public key format', async () => {
    const { getByTestId } = render(
      <WalletProvider>
        <TestComponent />
      </WalletProvider>
    );

    (PublicKey as jest.Mock).mockImplementation(() => {
      throw new Error('Invalid public key');
    });

    await act(async () => {
      fireEvent.press(getByTestId('connect'));
    });

    expect(getByTestId('publicKey').props.children).toBe('no-key');
    expect(getByTestId('isConnected').props.children).toBe('false');
    expect(AsyncStorage.setItem).not.toHaveBeenCalled();
  });

  it('throws error when useWallet is used outside provider', () => {
    const consoleError = console.error;
    console.error = jest.fn();

    expect(() => {
      render(<TestComponent />);
    }).toThrow('useWallet must be used within a WalletProvider');

    console.error = consoleError;
  });
}); 