import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react-native';
import ConnectWalletScreen from '../ConnectWalletScreen';
import { useWallet } from '../../context/WalletContext';
import { PublicKey } from '@solana/web3.js';

// Mock the hooks and services
jest.mock('../../context/WalletContext');
jest.mock('@solana/web3.js');

describe('ConnectWalletScreen', () => {
  const mockNavigation = {
    navigate: jest.fn(),
    goBack: jest.fn(),
  };

  beforeEach(() => {
    jest.clearAllMocks();
    (useWallet as jest.Mock).mockReturnValue({
      connectWallet: jest.fn(),
    });
  });

  it('renders connect wallet form', () => {
    const { getByText, getByPlaceholderText } = render(<ConnectWalletScreen />);
    
    expect(getByText('Connect Wallet')).toBeTruthy();
    expect(getByText('Enter your Solana wallet public key to view your balances and transactions')).toBeTruthy();
    expect(getByPlaceholderText('Enter your wallet public key')).toBeTruthy();
  });

  it('shows error for empty public key', async () => {
    const { getByText } = render(<ConnectWalletScreen />);
    
    fireEvent.press(getByText('Connect Wallet'));
    
    await waitFor(() => {
      expect(getByText('Please enter a public key')).toBeTruthy();
    });
  });

  it('shows error for invalid public key format', async () => {
    const mockConnectWallet = jest.fn();
    (useWallet as jest.Mock).mockReturnValue({
      connectWallet: mockConnectWallet,
    });

    (PublicKey as jest.Mock).mockImplementation(() => {
      throw new Error('Invalid public key');
    });

    const { getByText, getByPlaceholderText } = render(<ConnectWalletScreen />);
    
    fireEvent.changeText(getByPlaceholderText('Enter your wallet public key'), 'invalid-key');
    fireEvent.press(getByText('Connect Wallet'));
    
    await waitFor(() => {
      expect(getByText('Invalid public key format')).toBeTruthy();
    });
  });

  it('connects wallet with valid public key', async () => {
    const mockConnectWallet = jest.fn();
    const mockPublicKey = 'validPublicKey123';
    
    (useWallet as jest.Mock).mockReturnValue({
      connectWallet: mockConnectWallet,
    });

    const { getByText, getByPlaceholderText } = render(<ConnectWalletScreen />);
    
    fireEvent.changeText(getByPlaceholderText('Enter your wallet public key'), mockPublicKey);
    fireEvent.press(getByText('Connect Wallet'));
    
    await waitFor(() => {
      expect(mockConnectWallet).toHaveBeenCalledWith(mockPublicKey);
    });
  });

  it('handles cancel button', () => {
    const { getByText } = render(<ConnectWalletScreen />);
    
    fireEvent.press(getByText('Cancel'));
    
    expect(mockNavigation.goBack).toHaveBeenCalled();
  });

  it('disables buttons while loading', async () => {
    const mockConnectWallet = jest.fn().mockImplementation(() => new Promise(resolve => setTimeout(resolve, 100)));
    (useWallet as jest.Mock).mockReturnValue({
      connectWallet: mockConnectWallet,
    });

    const { getByText, getByPlaceholderText } = render(<ConnectWalletScreen />);
    
    fireEvent.changeText(getByPlaceholderText('Enter your wallet public key'), 'validPublicKey123');
    fireEvent.press(getByText('Connect Wallet'));
    
    expect(getByText('Connect Wallet')).toBeDisabled();
    expect(getByText('Cancel')).toBeDisabled();
  });
}); 