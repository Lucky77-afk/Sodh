import React from 'react';
import { render, fireEvent } from '@testing-library/react-native';
import SettingsScreen from '../SettingsScreen';
import { useWallet } from '../../context/WalletContext';

// Mock the hooks
jest.mock('../../context/WalletContext');

describe('SettingsScreen', () => {
  const mockDisconnectWallet = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
    (useWallet as jest.Mock).mockReturnValue({
      publicKey: 'mockPublicKey123',
      isConnected: true,
      disconnectWallet: mockDisconnectWallet,
    });
  });

  it('renders settings screen', () => {
    const { getByText } = render(<SettingsScreen />);

    expect(getByText('Settings')).toBeTruthy();
    expect(getByText('Wallet')).toBeTruthy();
    expect(getByText('Network')).toBeTruthy();
    expect(getByText('About')).toBeTruthy();
  });

  it('displays connected wallet info', () => {
    const { getByText } = render(<SettingsScreen />);

    expect(getByText('Connected Wallet')).toBeTruthy();
    expect(getByText('mockPublicKey123')).toBeTruthy();
  });

  it('displays network options', () => {
    const { getByText } = render(<SettingsScreen />);

    expect(getByText('Mainnet Beta')).toBeTruthy();
    expect(getByText('Testnet')).toBeTruthy();
    expect(getByText('Devnet')).toBeTruthy();
  });

  it('displays about information', () => {
    const { getByText } = render(<SettingsScreen />);

    expect(getByText('Version')).toBeTruthy();
    expect(getByText('1.0.0')).toBeTruthy();
  });

  it('handles wallet disconnect', () => {
    const { getByText } = render(<SettingsScreen />);

    fireEvent.press(getByText('Disconnect Wallet'));

    expect(mockDisconnectWallet).toHaveBeenCalled();
  });

  it('handles network change', () => {
    const { getByText } = render(<SettingsScreen />);

    fireEvent.press(getByText('Testnet'));

    expect(getByText('Network changed to Testnet')).toBeTruthy();
  });

  it('handles theme toggle', () => {
    const { getByText } = render(<SettingsScreen />);

    fireEvent.press(getByText('Dark Mode'));

    expect(getByText('Theme changed to Dark Mode')).toBeTruthy();
  });

  it('handles language change', () => {
    const { getByText } = render(<SettingsScreen />);

    fireEvent.press(getByText('Language'));

    expect(getByText('Language changed to English')).toBeTruthy();
  });
}); 