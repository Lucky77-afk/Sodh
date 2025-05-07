import React from 'react';
import { render, fireEvent } from '@testing-library/react-native';
import TransactionList from '../TransactionList';

describe('TransactionList', () => {
  const mockTransactions = [
    {
      signature: 'tx1',
      slot: 1,
      blockTime: 1234567890,
      status: 'success',
      fee: 0.000005,
    },
    {
      signature: 'tx2',
      slot: 2,
      blockTime: 1234567891,
      status: 'failed',
      fee: 0.000005,
    },
  ];

  const mockOnTransactionPress = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders transaction list', () => {
    const { getByText } = render(
      <TransactionList
        transactions={mockTransactions}
        onTransactionPress={mockOnTransactionPress}
      />
    );

    expect(getByText('Recent Transactions')).toBeTruthy();
    expect(getByText(mockTransactions[0].signature)).toBeTruthy();
    expect(getByText(mockTransactions[1].signature)).toBeTruthy();
  });

  it('handles empty transactions', () => {
    const { getByText } = render(
      <TransactionList transactions={[]} onTransactionPress={mockOnTransactionPress} />
    );

    expect(getByText('No transactions found')).toBeTruthy();
  });

  it('handles transaction press', () => {
    const { getByText } = render(
      <TransactionList
        transactions={mockTransactions}
        onTransactionPress={mockOnTransactionPress}
      />
    );

    fireEvent.press(getByText(mockTransactions[0].signature));

    expect(mockOnTransactionPress).toHaveBeenCalledWith(mockTransactions[0].signature);
  });

  it('renders transaction status', () => {
    const { getByText } = render(
      <TransactionList
        transactions={mockTransactions}
        onTransactionPress={mockOnTransactionPress}
      />
    );

    expect(getByText(`Status: ${mockTransactions[0].status}`)).toBeTruthy();
    expect(getByText(`Status: ${mockTransactions[1].status}`)).toBeTruthy();
  });

  it('renders transaction fee', () => {
    const { getByText } = render(
      <TransactionList
        transactions={mockTransactions}
        onTransactionPress={mockOnTransactionPress}
      />
    );

    expect(getByText(`Fee: ${mockTransactions[0].fee} SOL`)).toBeTruthy();
    expect(getByText(`Fee: ${mockTransactions[1].fee} SOL`)).toBeTruthy();
  });

  it('renders custom empty message', () => {
    const emptyMessage = 'No transactions available';
    const { getByText } = render(
      <TransactionList
        transactions={[]}
        onTransactionPress={mockOnTransactionPress}
        emptyMessage={emptyMessage}
      />
    );

    expect(getByText(emptyMessage)).toBeTruthy();
  });

  it('renders custom title', () => {
    const title = 'Transaction History';
    const { getByText } = render(
      <TransactionList
        transactions={mockTransactions}
        onTransactionPress={mockOnTransactionPress}
        title={title}
      />
    );

    expect(getByText(title)).toBeTruthy();
  });
}); 