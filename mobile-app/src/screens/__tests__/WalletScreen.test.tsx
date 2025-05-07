import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react-native';
import WalletScreen from '../WalletScreen';
import { useWallet } from '../../context/WalletContext';
import solanaService from '../../services/solana-service';

// Mock the hooks and services
jest.mock('../../context/WalletContext');
jest.mock('../../services/solana-service');

describe('WalletScreen', () => {
  const mockNavigation = {
    navigate: jest.fn(),
    goBack: jest.fn(),
  };

  beforeEach(() => {
    jest.clearAllMocks();
    (useWallet as jest.Mock).mockReturnValue({
      publicKey: null,
      isConnected: false,
      disconnectWallet: jest.fn(),
    });
  });

  it('renders connect wallet screen when not connected', () => {
    const { getByText } = render(<WalletScreen />);
    
    expect(getByText('No Wallet Connected')).toBeTruthy();
    expect(getByText('Connect a wallet to view your balances and transactions')).toBeTruthy();
    expect(getByText('Connect Wallet')).toBeTruthy();
  });

  it('renders wallet info when connected', async () => {
    const mockPublicKey = 'mockPublicKey123';
    const mockBalance = 1.5;
    const mockTransactions = [
      { signature: 'tx1', slot: 1, blockTime: 1234567890, status: 'success', fee: 0.000005 },
    ];

    (useWallet as jest.Mock).mockReturnValue({
      publicKey: mockPublicKey,
      isConnected: true,
      disconnectWallet: jest.fn(),
    });

    (solanaService.getBalance as jest.Mock).mockResolvedValue(mockBalance);
    (solanaService.getTransactionHistory as jest.Mock).mockResolvedValue(mockTransactions);

    const { getByText, getByTestId } = render(<WalletScreen />);

    await waitFor(() => {
      expect(getByText(mockPublicKey)).toBeTruthy();
      expect(getByText(mockBalance.toFixed(4))).toBeTruthy();
      expect(getByText('Recent Transactions')).toBeTruthy();
    });
  });

  it('handles wallet disconnect', async () => {
    const mockDisconnectWallet = jest.fn();
    (useWallet as jest.Mock).mockReturnValue({
      publicKey: 'mockPublicKey123',
      isConnected: true,
      disconnectWallet: mockDisconnectWallet,
    });

    const { getByText } = render(<WalletScreen />);
    
    fireEvent.press(getByText('Disconnect'));
    
    await waitFor(() => {
      expect(mockDisconnectWallet).toHaveBeenCalled();
    });
  });

  it('copies public key to clipboard', async () => {
    const mockPublicKey = 'mockPublicKey123';
    (useWallet as jest.Mock).mockReturnValue({
      publicKey: mockPublicKey,
      isConnected: true,
      disconnectWallet: jest.fn(),
    });

    const { getByText } = render(<WalletScreen />);
    
    fireEvent.press(getByText(mockPublicKey));
    
    await waitFor(() => {
      expect(require('expo-clipboard').setStringAsync).toHaveBeenCalledWith(mockPublicKey);
    });
  });

  it('handles error when fetching wallet data', async () => {
    const mockPublicKey = 'mockPublicKey123';
    (useWallet as jest.Mock).mockReturnValue({
      publicKey: mockPublicKey,
      isConnected: true,
      disconnectWallet: jest.fn(),
    });

    (solanaService.getBalance as jest.Mock).mockRejectedValue(new Error('Network error'));

    const { getByText } = render(<WalletScreen />);

    await waitFor(() => {
      expect(getByText('Failed to fetch wallet data. Please try again.')).toBeTruthy();
    });
  });
}); 