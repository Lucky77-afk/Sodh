import React from 'react';
import { render } from '@testing-library/react-native';
import { NavigationContainer } from '@react-navigation/native';
import AppNavigation from '../AppNavigation';

// Mock the screens
jest.mock('../../screens/HomeScreen', () => 'HomeScreen');
jest.mock('../../screens/ExplorerScreen', () => 'ExplorerScreen');
jest.mock('../../screens/WalletScreen', () => 'WalletScreen');
jest.mock('../../screens/SettingsScreen', () => 'SettingsScreen');
jest.mock('../../screens/ConnectWalletScreen', () => 'ConnectWalletScreen');
jest.mock('../../screens/TransactionDetailScreen', () => 'TransactionDetailScreen');

describe('AppNavigation', () => {
  it('renders navigation container', () => {
    const { getByTestId } = render(
      <NavigationContainer>
        <AppNavigation />
      </NavigationContainer>
    );

    expect(getByTestId('navigation-container')).toBeTruthy();
  });

  it('renders tab navigator', () => {
    const { getByTestId } = render(
      <NavigationContainer>
        <AppNavigation />
      </NavigationContainer>
    );

    expect(getByTestId('tab-navigator')).toBeTruthy();
  });

  it('renders all tab screens', () => {
    const { getByText } = render(
      <NavigationContainer>
        <AppNavigation />
      </NavigationContainer>
    );

    expect(getByText('Home')).toBeTruthy();
    expect(getByText('Explorer')).toBeTruthy();
    expect(getByText('Wallet')).toBeTruthy();
    expect(getByText('Settings')).toBeTruthy();
  });

  it('renders stack screens', () => {
    const { getByTestId } = render(
      <NavigationContainer>
        <AppNavigation />
      </NavigationContainer>
    );

    expect(getByTestId('stack-navigator')).toBeTruthy();
  });
}); 