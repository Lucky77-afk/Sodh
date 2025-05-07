import React from 'react';
import { render, fireEvent } from '@testing-library/react-native';
import WalletInfo from '../WalletInfo';

describe('WalletInfo', () => {
  const mockPublicKey = 'mockPublicKey123';
  const mockBalance = 1.5;
  const mockOnDisconnect = jest.fn();
  const mockOnViewWallet = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders wallet info', () => {
    const { getByText } = render(
      <WalletInfo
        publicKey={mockPublicKey}
        balance={mockBalance}
        onDisconnect={mockOnDisconnect}
        onViewWallet={mockOnViewWallet}
      />
    );

    expect(getByText('Wallet')).toBeTruthy();
    expect(getByText(mockPublicKey)).toBeTruthy();
    expect(getByText(`${mockBalance} SOL`)).toBeTruthy();
  });

  it('handles disconnect', () => {
    const { getByText } = render(
      <WalletInfo
        publicKey={mockPublicKey}
        balance={mockBalance}
        onDisconnect={mockOnDisconnect}
        onViewWallet={mockOnViewWallet}
      />
    );

    fireEvent.press(getByText('Disconnect'));

    expect(mockOnDisconnect).toHaveBeenCalled();
  });

  it('handles view wallet', () => {
    const { getByText } = render(
      <WalletInfo
        publicKey={mockPublicKey}
        balance={mockBalance}
        onDisconnect={mockOnDisconnect}
        onViewWallet={mockOnViewWallet}
      />
    );

    fireEvent.press(getByText('View Wallet'));

    expect(mockOnViewWallet).toHaveBeenCalled();
  });

  it('renders custom title', () => {
    const title = 'My Wallet';
    const { getByText } = render(
      <WalletInfo
        publicKey={mockPublicKey}
        balance={mockBalance}
        onDisconnect={mockOnDisconnect}
        onViewWallet={mockOnViewWallet}
        title={title}
      />
    );

    expect(getByText(title)).toBeTruthy();
  });

  it('renders custom disconnect text', () => {
    const disconnectText = 'Sign Out';
    const { getByText } = render(
      <WalletInfo
        publicKey={mockPublicKey}
        balance={mockBalance}
        onDisconnect={mockOnDisconnect}
        onViewWallet={mockOnViewWallet}
        disconnectText={disconnectText}
      />
    );

    expect(getByText(disconnectText)).toBeTruthy();
  });

  it('renders custom view wallet text', () => {
    const viewWalletText = 'Open Wallet';
    const { getByText } = render(
      <WalletInfo
        publicKey={mockPublicKey}
        balance={mockBalance}
        onDisconnect={mockOnDisconnect}
        onViewWallet={mockOnViewWallet}
        viewWalletText={viewWalletText}
      />
    );

    expect(getByText(viewWalletText)).toBeTruthy();
  });

  it('renders custom balance label', () => {
    const balanceLabel = 'Available Balance';
    const { getByText } = render(
      <WalletInfo
        publicKey={mockPublicKey}
        balance={mockBalance}
        onDisconnect={mockOnDisconnect}
        onViewWallet={mockOnViewWallet}
        balanceLabel={balanceLabel}
      />
    );

    expect(getByText(balanceLabel)).toBeTruthy();
  });
}); 