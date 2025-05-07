import React from 'react';
import { render, fireEvent } from '@testing-library/react-native';
import SearchBar from '../SearchBar';

describe('SearchBar', () => {
  const mockOnSearch = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders search bar', () => {
    const { getByPlaceholderText, getByText } = render(
      <SearchBar onSearch={mockOnSearch} />
    );

    expect(getByPlaceholderText('Enter public key or transaction signature')).toBeTruthy();
    expect(getByText('Search')).toBeTruthy();
  });

  it('handles search', () => {
    const { getByPlaceholderText, getByText } = render(
      <SearchBar onSearch={mockOnSearch} />
    );

    const input = getByPlaceholderText('Enter public key or transaction signature');
    fireEvent.changeText(input, 'mockPublicKey123');
    fireEvent.press(getByText('Search'));

    expect(mockOnSearch).toHaveBeenCalledWith('mockPublicKey123');
  });

  it('handles empty search', () => {
    const { getByPlaceholderText, getByText } = render(
      <SearchBar onSearch={mockOnSearch} />
    );

    fireEvent.press(getByText('Search'));

    expect(mockOnSearch).not.toHaveBeenCalled();
  });

  it('renders custom placeholder', () => {
    const placeholder = 'Search by address or signature';
    const { getByPlaceholderText } = render(
      <SearchBar onSearch={mockOnSearch} placeholder={placeholder} />
    );

    expect(getByPlaceholderText(placeholder)).toBeTruthy();
  });

  it('renders custom button text', () => {
    const buttonText = 'Find';
    const { getByText } = render(
      <SearchBar onSearch={mockOnSearch} buttonText={buttonText} />
    );

    expect(getByText(buttonText)).toBeTruthy();
  });

  it('handles input change', () => {
    const { getByPlaceholderText } = render(
      <SearchBar onSearch={mockOnSearch} />
    );

    const input = getByPlaceholderText('Enter public key or transaction signature');
    fireEvent.changeText(input, 'mockPublicKey123');

    expect(input.props.value).toBe('mockPublicKey123');
  });

  it('handles input clear', () => {
    const { getByPlaceholderText } = render(
      <SearchBar onSearch={mockOnSearch} />
    );

    const input = getByPlaceholderText('Enter public key or transaction signature');
    fireEvent.changeText(input, 'mockPublicKey123');
    fireEvent.changeText(input, '');

    expect(input.props.value).toBe('');
  });

  it('handles input focus', () => {
    const { getByPlaceholderText } = render(
      <SearchBar onSearch={mockOnSearch} />
    );

    const input = getByPlaceholderText('Enter public key or transaction signature');
    fireEvent.focus(input);

    expect(input.props.isFocused).toBe(true);
  });

  it('handles input blur', () => {
    const { getByPlaceholderText } = render(
      <SearchBar onSearch={mockOnSearch} />
    );

    const input = getByPlaceholderText('Enter public key or transaction signature');
    fireEvent.focus(input);
    fireEvent.blur(input);

    expect(input.props.isFocused).toBe(false);
  });
}); 