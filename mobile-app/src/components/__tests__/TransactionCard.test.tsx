import React from 'react';
import { render, fireEvent } from '@testing-library/react-native';
import TransactionCard from '../TransactionCard';

describe('TransactionCard', () => {
  const mockTransaction = {
    signature: 'tx1',
    slot: 1,
    blockTime: 1234567890,
    status: 'success',
    fee: 0.000005,
  };

  const mockOnPress = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders transaction card', () => {
    const { getByText } = render(
      <TransactionCard transaction={mockTransaction} onPress={mockOnPress} />
    );

    expect(getByText(mockTransaction.signature)).toBeTruthy();
    expect(getByText(`Status: ${mockTransaction.status}`)).toBeTruthy();
    expect(getByText(`Fee: ${mockTransaction.fee} SOL`)).toBeTruthy();
  });

  it('handles press', () => {
    const { getByText } = render(
      <TransactionCard transaction={mockTransaction} onPress={mockOnPress} />
    );

    fireEvent.press(getByText(mockTransaction.signature));

    expect(mockOnPress).toHaveBeenCalledWith(mockTransaction.signature);
  });

  it('renders custom status label', () => {
    const statusLabel = 'Transaction Status';
    const { getByText } = render(
      <TransactionCard
        transaction={mockTransaction}
        onPress={mockOnPress}
        statusLabel={statusLabel}
      />
    );

    expect(getByText(`${statusLabel}: ${mockTransaction.status}`)).toBeTruthy();
  });

  it('renders custom fee label', () => {
    const feeLabel = 'Transaction Fee';
    const { getByText } = render(
      <TransactionCard
        transaction={mockTransaction}
        onPress={mockOnPress}
        feeLabel={feeLabel}
      />
    );

    expect(getByText(`${feeLabel}: ${mockTransaction.fee} SOL`)).toBeTruthy();
  });

  it('renders custom time format', () => {
    const timeFormat = 'MM/DD/YYYY';
    const { getByText } = render(
      <TransactionCard
        transaction={mockTransaction}
        onPress={mockOnPress}
        timeFormat={timeFormat}
      />
    );

    expect(
      getByText(
        new Date(mockTransaction.blockTime * 1000).toLocaleDateString('en-US', {
          month: '2-digit',
          day: '2-digit',
          year: 'numeric',
        })
      )
    ).toBeTruthy();
  });

  it('renders custom signature label', () => {
    const signatureLabel = 'Transaction ID';
    const { getByText } = render(
      <TransactionCard
        transaction={mockTransaction}
        onPress={mockOnPress}
        signatureLabel={signatureLabel}
      />
    );

    expect(getByText(`${signatureLabel}: ${mockTransaction.signature}`)).toBeTruthy();
  });

  it('renders custom slot label', () => {
    const slotLabel = 'Block Number';
    const { getByText } = render(
      <TransactionCard
        transaction={mockTransaction}
        onPress={mockOnPress}
        slotLabel={slotLabel}
      />
    );

    expect(getByText(`${slotLabel}: ${mockTransaction.slot}`)).toBeTruthy();
  });

  it('renders custom block time label', () => {
    const blockTimeLabel = 'Block Time';
    const { getByText } = render(
      <TransactionCard
        transaction={mockTransaction}
        onPress={mockOnPress}
        blockTimeLabel={blockTimeLabel}
      />
    );

    expect(
      getByText(
        `${blockTimeLabel}: ${new Date(mockTransaction.blockTime * 1000).toLocaleString()}`
      )
    ).toBeTruthy();
  });
}); 