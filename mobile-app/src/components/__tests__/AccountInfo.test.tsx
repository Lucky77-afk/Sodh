import React from 'react';
import { render } from '@testing-library/react-native';
import AccountInfo from '../AccountInfo';

describe('AccountInfo', () => {
  const mockAccount = {
    publicKey: 'mockPublicKey123',
    balance: 1.5,
    owner: 'System Program',
    executable: false,
    rentEpoch: 0,
  };

  it('renders account info', () => {
    const { getByText } = render(<AccountInfo account={mockAccount} />);

    expect(getByText('Account Information')).toBeTruthy();
    expect(getByText(mockAccount.publicKey)).toBeTruthy();
    expect(getByText(`${mockAccount.balance} SOL`)).toBeTruthy();
    expect(getByText(`Owner: ${mockAccount.owner}`)).toBeTruthy();
    expect(getByText(`Executable: ${mockAccount.executable}`)).toBeTruthy();
    expect(getByText(`Rent Epoch: ${mockAccount.rentEpoch}`)).toBeTruthy();
  });

  it('renders custom title', () => {
    const title = 'Wallet Details';
    const { getByText } = render(<AccountInfo account={mockAccount} title={title} />);

    expect(getByText(title)).toBeTruthy();
  });

  it('renders custom public key label', () => {
    const publicKeyLabel = 'Address';
    const { getByText } = render(
      <AccountInfo account={mockAccount} publicKeyLabel={publicKeyLabel} />
    );

    expect(getByText(`${publicKeyLabel}: ${mockAccount.publicKey}`)).toBeTruthy();
  });

  it('renders custom balance label', () => {
    const balanceLabel = 'Available Balance';
    const { getByText } = render(
      <AccountInfo account={mockAccount} balanceLabel={balanceLabel} />
    );

    expect(getByText(`${balanceLabel}: ${mockAccount.balance} SOL`)).toBeTruthy();
  });

  it('renders custom owner label', () => {
    const ownerLabel = 'Program Owner';
    const { getByText } = render(
      <AccountInfo account={mockAccount} ownerLabel={ownerLabel} />
    );

    expect(getByText(`${ownerLabel}: ${mockAccount.owner}`)).toBeTruthy();
  });

  it('renders custom executable label', () => {
    const executableLabel = 'Is Program';
    const { getByText } = render(
      <AccountInfo account={mockAccount} executableLabel={executableLabel} />
    );

    expect(getByText(`${executableLabel}: ${mockAccount.executable}`)).toBeTruthy();
  });

  it('renders custom rent epoch label', () => {
    const rentEpochLabel = 'Current Epoch';
    const { getByText } = render(
      <AccountInfo account={mockAccount} rentEpochLabel={rentEpochLabel} />
    );

    expect(getByText(`${rentEpochLabel}: ${mockAccount.rentEpoch}`)).toBeTruthy();
  });

  it('renders loading state', () => {
    const { getByText } = render(<AccountInfo account={null} />);

    expect(getByText('Loading account information...')).toBeTruthy();
  });

  it('renders error state', () => {
    const { getByText } = render(<AccountInfo account={null} error="Network error" />);

    expect(getByText('Failed to fetch account information')).toBeTruthy();
  });

  it('renders custom loading text', () => {
    const loadingText = 'Fetching account details...';
    const { getByText } = render(<AccountInfo account={null} loadingText={loadingText} />);

    expect(getByText(loadingText)).toBeTruthy();
  });

  it('renders custom error text', () => {
    const errorText = 'Account not found';
    const { getByText } = render(
      <AccountInfo account={null} error="Network error" errorText={errorText} />
    );

    expect(getByText(errorText)).toBeTruthy();
  });
}); 