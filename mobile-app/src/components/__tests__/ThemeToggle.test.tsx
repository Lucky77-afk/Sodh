import React from 'react';
import { render, fireEvent } from '@testing-library/react-native';
import ThemeToggle from '../ThemeToggle';

describe('ThemeToggle', () => {
  const mockOnToggle = jest.fn();

  beforeEach(() => {
    jest.clearAllMocks();
  });

  it('renders theme toggle', () => {
    const { getByText } = render(<ThemeToggle onToggle={mockOnToggle} />);

    expect(getByText('Dark Mode')).toBeTruthy();
  });

  it('handles toggle', () => {
    const { getByText } = render(<ThemeToggle onToggle={mockOnToggle} />);

    fireEvent.press(getByText('Dark Mode'));

    expect(mockOnToggle).toHaveBeenCalled();
  });

  it('renders custom label', () => {
    const label = 'Toggle Theme';
    const { getByText } = render(<ThemeToggle onToggle={mockOnToggle} label={label} />);

    expect(getByText(label)).toBeTruthy();
  });

  it('renders custom icon', () => {
    const icon = 'moon';
    const { getByTestId } = render(<ThemeToggle onToggle={mockOnToggle} icon={icon} />);

    expect(getByTestId('theme-icon')).toBeTruthy();
  });

  it('renders custom colors', () => {
    const colors = {
      light: '#FFFFFF',
      dark: '#000000',
    };

    const { getByTestId } = render(
      <ThemeToggle onToggle={mockOnToggle} colors={colors} />
    );

    const toggle = getByTestId('theme-toggle');
    expect(toggle.props.style).toContainEqual({ backgroundColor: colors.light });
  });

  it('renders custom size', () => {
    const size = 50;
    const { getByTestId } = render(<ThemeToggle onToggle={mockOnToggle} size={size} />);

    const toggle = getByTestId('theme-toggle');
    expect(toggle.props.style).toContainEqual({ width: size, height: size });
  });

  it('renders custom position', () => {
    const position = { top: 20, right: 20 };
    const { getByTestId } = render(
      <ThemeToggle onToggle={mockOnToggle} position={position} />
    );

    const toggle = getByTestId('theme-toggle');
    expect(toggle.props.style).toContainEqual(position);
  });

  it('renders custom animation', () => {
    const animation = { duration: 500, easing: 'ease-in-out' };
    const { getByTestId } = render(
      <ThemeToggle onToggle={mockOnToggle} animation={animation} />
    );

    const toggle = getByTestId('theme-toggle');
    expect(toggle.props.style).toContainEqual({ transition: `all ${animation.duration}ms ${animation.easing}` });
  });

  it('renders custom accessibility label', () => {
    const accessibilityLabel = 'Toggle dark mode';
    const { getByLabelText } = render(
      <ThemeToggle onToggle={mockOnToggle} accessibilityLabel={accessibilityLabel} />
    );

    expect(getByLabelText(accessibilityLabel)).toBeTruthy();
  });

  it('renders custom accessibility hint', () => {
    const accessibilityHint = 'Double tap to toggle dark mode';
    const { getByHintText } = render(
      <ThemeToggle onToggle={mockOnToggle} accessibilityHint={accessibilityHint} />
    );

    expect(getByHintText(accessibilityHint)).toBeTruthy();
  });
}); 