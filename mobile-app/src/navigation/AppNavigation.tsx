import React from 'react';
import { NavigationContainer } from '@react-navigation/native';
import { createStackNavigator } from '@react-navigation/stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { MaterialCommunityIcons } from '@expo/vector-icons';

// Import your screens
import HomeScreen from '../screens/HomeScreen';
import ExplorerScreen from '../screens/ExplorerScreen';
import WalletScreen from '../screens/WalletScreen';
import TransactionDetailScreen from '../screens/TransactionDetailScreen';
import SettingsScreen from '../screens/SettingsScreen';
import ConnectWalletScreen from '../screens/ConnectWalletScreen';

// Create stack navigator
const Stack = createStackNavigator();
const Tab = createBottomTabNavigator();

// Define tab navigator
const TabNavigator = () => {
  return (
    <Tab.Navigator
      screenOptions={{
        tabBarActiveTintColor: '#512DA8',
        tabBarInactiveTintColor: '#757575',
        tabBarStyle: {
          backgroundColor: '#121212',
          borderTopColor: '#2c2c2c',
        },
        headerStyle: {
          backgroundColor: '#121212',
        },
        headerTintColor: '#FFFFFF',
      }}
    >
      <Tab.Screen
        name="Home"
        component={HomeScreen}
        options={{
          tabBarIcon: ({ color, size }) => (
            <MaterialCommunityIcons name="home" color={color} size={size} />
          ),
        }}
      />
      <Tab.Screen
        name="Explorer"
        component={ExplorerScreen}
        options={{
          tabBarIcon: ({ color, size }) => (
            <MaterialCommunityIcons name="magnify" color={color} size={size} />
          ),
        }}
      />
      <Tab.Screen
        name="Wallet"
        component={WalletScreen}
        options={{
          tabBarIcon: ({ color, size }) => (
            <MaterialCommunityIcons name="wallet" color={color} size={size} />
          ),
        }}
      />
      <Tab.Screen
        name="Settings"
        component={SettingsScreen}
        options={{
          tabBarIcon: ({ color, size }) => (
            <MaterialCommunityIcons name="cog" color={color} size={size} />
          ),
        }}
      />
    </Tab.Navigator>
  );
};

// Main navigation container
const AppNavigation = () => {
  return (
    <NavigationContainer>
      <Stack.Navigator
        screenOptions={{
          headerStyle: {
            backgroundColor: '#121212',
          },
          headerTintColor: '#FFFFFF',
          cardStyle: { backgroundColor: '#1E1E1E' },
        }}
      >
        <Stack.Screen
          name="MainTabs"
          component={TabNavigator}
          options={{ headerShown: false }}
        />
        <Stack.Screen
          name="TransactionDetail"
          component={TransactionDetailScreen}
          options={{ title: 'Transaction Details' }}
        />
        <Stack.Screen
          name="ConnectWallet"
          component={ConnectWalletScreen}
          options={{ title: 'Connect Wallet' }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

export default AppNavigation; 