import React from 'react';
import { render, fireEvent } from '@testing-library/react-native';
import NetworkSelector from '../NetworkSelector';

describe('NetworkSelector', () => {
  const mockNetworks = [
    { id: 'mainnet-beta', name: 'Mainnet Beta' },
    { id: 'testnet', name: 'Testnet' },
    { id: 'devnet', name: 'Devnet' },
  ];

  const mockOnSelect = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders network selector', () => {
    const { getByText } = render(
      <NetworkSelector networks={mockNetworks} onSelect={mockOnSelect} />
    );

    expect(getByText('Select Network')).toBeTruthy();
    mockNetworks.forEach(network => {
      expect(getByText(network.name)).toBeTruthy();
    });
  });

  it('handles network selection', () => {
    const { getByText } = render(
      <NetworkSelector networks={mockNetworks} onSelect={mockOnSelect} />
    );

    fireEvent.press(getByText(mockNetworks[0].name));

    expect(mockOnSelect).toHaveBeenCalledWith(mockNetworks[0].id);
  });

  it('renders custom title', () => {
    const title = 'Choose Network';
    const { getByText } = render(
      <NetworkSelector networks={mockNetworks} onSelect={mockOnSelect} title={title} />
    );

    expect(getByText(title)).toBeTruthy();
  });

  it('renders selected network', () => {
    const selectedNetwork = 'mainnet-beta';
    const { getByText } = render(
      <NetworkSelector
        networks={mockNetworks}
        onSelect={mockOnSelect}
        selectedNetwork={selectedNetwork}
      />
    );

    const selectedNetworkItem = getByText(mockNetworks[0].name);
    expect(selectedNetworkItem.props.style).toContainEqual({ fontWeight: 'bold' });
  });

  it('renders custom network names', () => {
    const customNetworks = [
      { id: 'mainnet-beta', name: 'Production' },
      { id: 'testnet', name: 'Testing' },
      { id: 'devnet', name: 'Development' },
    ];

    const { getByText } = render(
      <NetworkSelector networks={customNetworks} onSelect={mockOnSelect} />
    );

    customNetworks.forEach(network => {
      expect(getByText(network.name)).toBeTruthy();
    });
  });

  it('handles empty networks', () => {
    const { getByText } = render(
      <NetworkSelector networks={[]} onSelect={mockOnSelect} />
    );

    expect(getByText('No networks available')).toBeTruthy();
  });

  it('renders custom empty message', () => {
    const emptyMessage = 'No networks configured';
    const { getByText } = render(
      <NetworkSelector networks={[]} onSelect={mockOnSelect} emptyMessage={emptyMessage} />
    );

    expect(getByText(emptyMessage)).toBeTruthy();
  });

  it('renders network descriptions', () => {
    const networksWithDescriptions = [
      { id: 'mainnet-beta', name: 'Mainnet Beta', description: 'Production network' },
      { id: 'testnet', name: 'Testnet', description: 'Testing network' },
      { id: 'devnet', name: 'Devnet', description: 'Development network' },
    ];

    const { getByText } = render(
      <NetworkSelector networks={networksWithDescriptions} onSelect={mockOnSelect} />
    );

    networksWithDescriptions.forEach(network => {
      expect(getByText(network.description)).toBeTruthy();
    });
  });
}); 