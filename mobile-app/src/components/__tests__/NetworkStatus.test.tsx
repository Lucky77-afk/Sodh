import React from 'react';
import { render } from '@testing-library/react-native';
import NetworkStatus from '../NetworkStatus';

describe('NetworkStatus', () => {
  const mockNetworkStatus = {
    version: '1.0.0',
    slot: 12345,
    blockTime: 1234567890,
  };

  it('renders network status', () => {
    const { getByText } = render(<NetworkStatus status={mockNetworkStatus} />);

    expect(getByText('Network Status')).toBeTruthy();
    expect(getByText(`Version: ${mockNetworkStatus.version}`)).toBeTruthy();
    expect(getByText(`Slot: ${mockNetworkStatus.slot}`)).toBeTruthy();
    expect(getByText(`Block Time: ${new Date(mockNetworkStatus.blockTime * 1000).toLocaleString()}`)).toBeTruthy();
  });

  it('renders loading state', () => {
    const { getByText } = render(<NetworkStatus status={null} />);

    expect(getByText('Loading network status...')).toBeTruthy();
  });

  it('renders error state', () => {
    const { getByText } = render(<NetworkStatus status={null} error="Network error" />);

    expect(getByText('Failed to fetch network status')).toBeTruthy();
  });

  it('renders custom title', () => {
    const title = 'Solana Network';
    const { getByText } = render(<NetworkStatus status={mockNetworkStatus} title={title} />);

    expect(getByText(title)).toBeTruthy();
  });

  it('renders custom loading text', () => {
    const loadingText = 'Checking network...';
    const { getByText } = render(<NetworkStatus status={null} loadingText={loadingText} />);

    expect(getByText(loadingText)).toBeTruthy();
  });

  it('renders custom error text', () => {
    const errorText = 'Network connection failed';
    const { getByText } = render(
      <NetworkStatus status={null} error="Network error" errorText={errorText} />
    );

    expect(getByText(errorText)).toBeTruthy();
  });

  it('renders custom version label', () => {
    const versionLabel = 'Node Version';
    const { getByText } = render(
      <NetworkStatus status={mockNetworkStatus} versionLabel={versionLabel} />
    );

    expect(getByText(`${versionLabel}: ${mockNetworkStatus.version}`)).toBeTruthy();
  });

  it('renders custom slot label', () => {
    const slotLabel = 'Current Slot';
    const { getByText } = render(
      <NetworkStatus status={mockNetworkStatus} slotLabel={slotLabel} />
    );

    expect(getByText(`${slotLabel}: ${mockNetworkStatus.slot}`)).toBeTruthy();
  });

  it('renders custom block time label', () => {
    const blockTimeLabel = 'Last Block';
    const { getByText } = render(
      <NetworkStatus status={mockNetworkStatus} blockTimeLabel={blockTimeLabel} />
    );

    expect(
      getByText(
        `${blockTimeLabel}: ${new Date(mockNetworkStatus.blockTime * 1000).toLocaleString()}`
      )
    ).toBeTruthy();
  });
}); 