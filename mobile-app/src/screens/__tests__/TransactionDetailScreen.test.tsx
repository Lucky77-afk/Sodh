import React from 'react';
import { render, waitFor } from '@testing-library/react-native';
import TransactionDetailScreen from '../TransactionDetailScreen';
import solanaService from '../../services/solana-service';

// Mock the services
jest.mock('../../services/solana-service');

describe('TransactionDetailScreen', () => {
  const mockRoute = {
    params: {
      signature: 'tx1',
    },
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders transaction details', async () => {
    const mockTransaction = {
      signature: 'tx1',
      slot: 1,
      blockTime: 1234567890,
      status: 'success',
      fee: 0.000005,
      from: 'fromAddress123',
      to: 'toAddress456',
      amount: 1.5,
    };

    (solanaService.getTransactionDetails as jest.Mock).mockResolvedValue(mockTransaction);

    const { getByText } = render(<TransactionDetailScreen route={mockRoute} />);

    await waitFor(() => {
      expect(getByText('Transaction Details')).toBeTruthy();
      expect(getByText(mockTransaction.signature)).toBeTruthy();
      expect(getByText(`Status: ${mockTransaction.status}`)).toBeTruthy();
      expect(getByText(`Fee: ${mockTransaction.fee} SOL`)).toBeTruthy();
      expect(getByText(`From: ${mockTransaction.from}`)).toBeTruthy();
      expect(getByText(`To: ${mockTransaction.to}`)).toBeTruthy();
      expect(getByText(`Amount: ${mockTransaction.amount} SOL`)).toBeTruthy();
    });
  });

  it('handles loading state', () => {
    const { getByText } = render(<TransactionDetailScreen route={mockRoute} />);

    expect(getByText('Loading...')).toBeTruthy();
  });

  it('handles error state', async () => {
    (solanaService.getTransactionDetails as jest.Mock).mockRejectedValue(new Error('Network error'));

    const { getByText } = render(<TransactionDetailScreen route={mockRoute} />);

    await waitFor(() => {
      expect(getByText('Failed to fetch transaction details')).toBeTruthy();
    });
  });

  it('handles missing signature', () => {
    const { getByText } = render(<TransactionDetailScreen route={{ params: {} }} />);

    expect(getByText('Transaction signature is required')).toBeTruthy();
  });
}); 