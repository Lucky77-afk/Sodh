import React from 'react';
import { render } from '@testing-library/react-native';
import ErrorBoundary from '../ErrorBoundary';

describe('ErrorBoundary', () => {
  const ThrowError = () => {
    throw new Error('Test error');
  };

  beforeEach(() => {
    jest.spyOn(console, 'error').mockImplementation(() => {});
  });

  afterEach(() => {
    jest.restoreAllMocks();
  });

  it('renders children when there is no error', () => {
    const { getByText } = render(
      <ErrorBoundary>
        <ThrowError />
      </ErrorBoundary>
    );

    expect(getByText('Something went wrong')).toBeTruthy();
    expect(getByText('Test error')).toBeTruthy();
  });

  it('renders error message when there is an error', () => {
    const { getByText } = render(
      <ErrorBoundary>
        <ThrowError />
      </ErrorBoundary>
    );

    expect(getByText('Something went wrong')).toBeTruthy();
    expect(getByText('Test error')).toBeTruthy();
  });

  it('renders retry button', () => {
    const { getByText } = render(
      <ErrorBoundary>
        <ThrowError />
      </ErrorBoundary>
    );

    expect(getByText('Retry')).toBeTruthy();
  });

  it('calls onRetry when retry button is pressed', () => {
    const onRetry = jest.fn();
    const { getByText } = render(
      <ErrorBoundary onRetry={onRetry}>
        <ThrowError />
      </ErrorBoundary>
    );

    getByText('Retry').props.onPress();

    expect(onRetry).toHaveBeenCalled();
  });

  it('renders custom error message', () => {
    const customMessage = 'Custom error message';
    const { getByText } = render(
      <ErrorBoundary errorMessage={customMessage}>
        <ThrowError />
      </ErrorBoundary>
    );

    expect(getByText(customMessage)).toBeTruthy();
  });

  it('renders custom retry button text', () => {
    const customRetryText = 'Try Again';
    const { getByText } = render(
      <ErrorBoundary retryButtonText={customRetryText}>
        <ThrowError />
      </ErrorBoundary>
    );

    expect(getByText(customRetryText)).toBeTruthy();
  });
}); 