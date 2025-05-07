import React from 'react';
import { render, fireEvent, waitFor } from '@testing-library/react-native';
import ExplorerScreen from '../ExplorerScreen';
import solanaService from '../../services/solana-service';

// Mock the services
jest.mock('../../services/solana-service');

describe('ExplorerScreen', () => {
  const mockNavigation = {
    navigate: jest.fn(),
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders search form', () => {
    const { getByPlaceholderText, getByText } = render(<ExplorerScreen />);

    expect(getByPlaceholderText('Enter public key or transaction signature')).toBeTruthy();
    expect(getByText('Search')).toBeTruthy();
  });

  it('searches for account', async () => {
    const mockPublicKey = 'mockPublicKey123';
    const mockBalance = 1.5;
    const mockTransactions = [
      {
        signature: 'tx1',
        slot: 1,
        blockTime: 1234567890,
        status: 'success',
        fee: 0.000005,
      },
    ];

    (solanaService.getBalance as jest.Mock).mockResolvedValue(mockBalance);
    (solanaService.getTransactionHistory as jest.Mock).mockResolvedValue(mockTransactions);

    const { getByPlaceholderText, getByText } = render(<ExplorerScreen />);

    fireEvent.changeText(
      getByPlaceholderText('Enter public key or transaction signature'),
      mockPublicKey
    );
    fireEvent.press(getByText('Search'));

    await waitFor(() => {
      expect(getByText('Account Information')).toBeTruthy();
      expect(getByText(`${mockBalance} SOL`)).toBeTruthy();
      expect(getByText('Recent Transactions')).toBeTruthy();
      expect(getByText(mockTransactions[0].signature)).toBeTruthy();
    });
  });

  it('searches for transaction', async () => {
    const mockSignature = 'tx1';
    const mockTransaction = {
      signature: 'tx1',
      slot: 1,
      blockTime: 1234567890,
      status: 'success',
      fee: 0.000005,
    };

    (solanaService.getTransactionDetails as jest.Mock).mockResolvedValue(mockTransaction);

    const { getByPlaceholderText, getByText } = render(<ExplorerScreen />);

    fireEvent.changeText(
      getByPlaceholderText('Enter public key or transaction signature'),
      mockSignature
    );
    fireEvent.press(getByText('Search'));

    await waitFor(() => {
      expect(getByText('Transaction Details')).toBeTruthy();
      expect(getByText(mockTransaction.signature)).toBeTruthy();
      expect(getByText(`Status: ${mockTransaction.status}`)).toBeTruthy();
      expect(getByText(`Fee: ${mockTransaction.fee} SOL`)).toBeTruthy();
    });
  });

  it('navigates to transaction detail', async () => {
    const mockPublicKey = 'mockPublicKey123';
    const mockTransactions = [
      {
        signature: 'tx1',
        slot: 1,
        blockTime: 1234567890,
        status: 'success',
        fee: 0.000005,
      },
    ];

    (solanaService.getBalance as jest.Mock).mockResolvedValue(1.5);
    (solanaService.getTransactionHistory as jest.Mock).mockResolvedValue(mockTransactions);

    const { getByPlaceholderText, getByText } = render(<ExplorerScreen />);

    fireEvent.changeText(
      getByPlaceholderText('Enter public key or transaction signature'),
      mockPublicKey
    );
    fireEvent.press(getByText('Search'));

    await waitFor(() => {
      fireEvent.press(getByText(mockTransactions[0].signature));
      expect(mockNavigation.navigate).toHaveBeenCalledWith('TransactionDetail', {
        signature: mockTransactions[0].signature,
      });
    });
  });

  it('handles search error', async () => {
    const mockPublicKey = 'mockPublicKey123';
    (solanaService.getBalance as jest.Mock).mockRejectedValue(new Error('Network error'));

    const { getByPlaceholderText, getByText } = render(<ExplorerScreen />);

    fireEvent.changeText(
      getByPlaceholderText('Enter public key or transaction signature'),
      mockPublicKey
    );
    fireEvent.press(getByText('Search'));

    await waitFor(() => {
      expect(getByText('Failed to fetch account information')).toBeTruthy();
    });
  });

  it('handles empty search', () => {
    const { getByPlaceholderText, getByText } = render(<ExplorerScreen />);

    fireEvent.press(getByText('Search'));

    expect(getByText('Please enter a public key or transaction signature')).toBeTruthy();
  });
}); 