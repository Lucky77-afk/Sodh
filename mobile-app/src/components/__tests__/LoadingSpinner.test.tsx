import React from 'react';
import { render } from '@testing-library/react-native';
import LoadingSpinner from '../LoadingSpinner';

describe('LoadingSpinner', () => {
  it('renders with default props', () => {
    const { getByTestId } = render(<LoadingSpinner />);

    expect(getByTestId('loading-spinner')).toBeTruthy();
  });

  it('renders with custom size', () => {
    const size = 50;
    const { getByTestId } = render(<LoadingSpinner size={size} />);

    const spinner = getByTestId('loading-spinner');
    expect(spinner.props.size).toBe(size);
  });

  it('renders with custom color', () => {
    const color = '#FF0000';
    const { getByTestId } = render(<LoadingSpinner color={color} />);

    const spinner = getByTestId('loading-spinner');
    expect(spinner.props.color).toBe(color);
  });

  it('renders with custom text', () => {
    const text = 'Loading...';
    const { getByText } = render(<LoadingSpinner text={text} />);

    expect(getByText(text)).toBeTruthy();
  });

  it('renders with custom text style', () => {
    const textStyle = { color: '#FF0000', fontSize: 16 };
    const { getByText } = render(<LoadingSpinner text="Loading..." textStyle={textStyle} />);

    const textElement = getByText('Loading...');
    expect(textElement.props.style).toContainEqual(textStyle);
  });

  it('renders with custom container style', () => {
    const containerStyle = { backgroundColor: '#000000' };
    const { getByTestId } = render(<LoadingSpinner containerStyle={containerStyle} />);

    const container = getByTestId('loading-spinner-container');
    expect(container.props.style).toContainEqual(containerStyle);
  });
}); 