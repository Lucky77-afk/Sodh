import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react-native';
import HomeScreen from '../HomeScreen';
import { useWallet } from '../../context/WalletContext';
import solanaService from '../../services/solana-service';

// Mock the hooks and services
jest.mock('../../context/WalletContext');
jest.mock('../../services/solana-service');

describe('HomeScreen', () => {
  const mockNavigation = {
    navigate: jest.fn(),
  };

  beforeEach(() => {
    jest.clearAllMocks();
    (useWallet as jest.Mock).mockReturnValue({
      publicKey: null,
      isConnected: false,
    });
  });

  it('renders home screen with network status', async () => {
    const mockNetworkStatus = {
      version: '1.0.0',
      slot: 12345,
      blockTime: 1234567890,
    };

    (solanaService.getNetworkStatus as jest.Mock).mockResolvedValue(mockNetworkStatus);

    const { getByText } = render(<HomeScreen />);

    await waitFor(() => {
      expect(getByText('Network Status')).toBeTruthy();
      expect(getByText(`Version: ${mockNetworkStatus.version}`)).toBeTruthy();
      expect(getByText(`Slot: ${mockNetworkStatus.slot}`)).toBeTruthy();
    });
  });

  it('renders connect wallet button when not connected', () => {
    const { getByText } = render(<HomeScreen />);

    expect(getByText('Connect Wallet')).toBeTruthy();
  });

  it('renders wallet info when connected', async () => {
    const mockPublicKey = 'mockPublicKey123';
    const mockBalance = 1.5;

    (useWallet as jest.Mock).mockReturnValue({
      publicKey: mockPublicKey,
      isConnected: true,
    });

    (solanaService.getBalance as jest.Mock).mockResolvedValue(mockBalance);

    const { getByText } = render(<HomeScreen />);

    await waitFor(() => {
      expect(getByText('Wallet')).toBeTruthy();
      expect(getByText(mockPublicKey)).toBeTruthy();
      expect(getByText(`${mockBalance} SOL`)).toBeTruthy();
    });
  });

  it('navigates to connect wallet screen', () => {
    const { getByText } = render(<HomeScreen />);

    fireEvent.press(getByText('Connect Wallet'));

    expect(mockNavigation.navigate).toHaveBeenCalledWith('ConnectWallet');
  });

  it('navigates to explorer screen', () => {
    const { getByText } = render(<HomeScreen />);

    fireEvent.press(getByText('Explore Blockchain'));

    expect(mockNavigation.navigate).toHaveBeenCalledWith('Explorer');
  });

  it('handles network status error', async () => {
    (solanaService.getNetworkStatus as jest.Mock).mockRejectedValue(new Error('Network error'));

    const { getByText } = render(<HomeScreen />);

    await waitFor(() => {
      expect(getByText('Failed to fetch network status')).toBeTruthy();
    });
  });

  it('handles wallet balance error', async () => {
    const mockPublicKey = 'mockPublicKey123';
    (useWallet as jest.Mock).mockReturnValue({
      publicKey: mockPublicKey,
      isConnected: true,
    });

    (solanaService.getBalance as jest.Mock).mockRejectedValue(new Error('Network error'));

    const { getByText } = render(<HomeScreen />);

    await waitFor(() => {
      expect(getByText('Failed to fetch wallet balance')).toBeTruthy();
    });
  });
}); 