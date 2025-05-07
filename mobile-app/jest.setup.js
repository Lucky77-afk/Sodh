import '@testing-library/jest-native/extend-expect';

// Mock AsyncStorage
jest.mock('@react-native-async-storage/async-storage', () =>
  require('@react-native-async-storage/async-storage/jest/async-storage-mock')
);

// Mock expo-clipboard
jest.mock('expo-clipboard', () => ({
  setStringAsync: jest.fn(),
  getStringAsync: jest.fn(),
}));

// Mock @solana/web3.js
jest.mock('@solana/web3.js', () => ({
  Connection: jest.fn(),
  PublicKey: jest.fn(),
  clusterApiUrl: jest.fn(),
}));

// Mock react-native-paper
jest.mock('react-native-paper', () => {
  const React = require('react');
  const { View } = require('react-native');
  
  return {
    Card: ({ children }) => <View>{children}</View>,
    Card.Content: ({ children }) => <View>{children}</View>,
    Title: ({ children }) => <View>{children}</View>,
    Paragraph: ({ children }) => <View>{children}</View>,
    Button: ({ children, onPress }) => (
      <View onPress={onPress}>{children}</View>
    ),
    TextInput: ({ children }) => <View>{children}</View>,
    HelperText: ({ children }) => <View>{children}</View>,
    ActivityIndicator: () => <View />,
    Divider: () => <View />,
    Avatar: {
      Icon: () => <View />,
    },
  };
});

// Mock @expo/vector-icons
jest.mock('@expo/vector-icons', () => ({
  MaterialCommunityIcons: 'MaterialCommunityIcons',
}));

// Mock react-navigation
jest.mock('@react-navigation/native', () => ({
  useNavigation: () => ({
    navigate: jest.fn(),
    goBack: jest.fn(),
  }),
})); 