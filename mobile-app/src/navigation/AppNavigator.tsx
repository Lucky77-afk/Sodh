import React from 'react';
import { NavigationContainer, DefaultTheme } from '@react-navigation/native';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import { createStackNavigator } from '@react-navigation/stack';
import { useTheme } from 'react-native-paper';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';

// Import screens
import DashboardScreen from '../screens/DashboardScreen';
import TransactionsScreen from '../screens/TransactionsScreen';
import AccountScreen from '../screens/AccountScreen';
import SmartContractScreen from '../screens/SmartContractScreen';
import WhitepaperScreen from '../screens/WhitepaperScreen';
import TutorialScreen from '../screens/TutorialScreen';
import ProjectDetailsScreen from '../screens/ProjectDetailsScreen';
import MilestoneDetailsScreen from '../screens/MilestoneDetailsScreen';
import TransactionDetailsScreen from '../screens/TransactionDetailsScreen';

// Stack navigator types
type RootStackParamList = {
  Main: undefined;
  ProjectDetails: { projectId: string };
  MilestoneDetails: { milestoneId: string, projectId: string };
  TransactionDetails: { signature: string };
};

// Tab navigator types
type MainTabParamList = {
  Dashboard: undefined;
  Transactions: undefined;
  Account: undefined;
  SmartContract: undefined;
  More: undefined;
};

// Create navigators
const Stack = createStackNavigator<RootStackParamList>();
const Tab = createBottomTabNavigator<MainTabParamList>();
const MoreStack = createStackNavigator();

// More menu stack (for Whitepaper and Tutorial)
const MoreStackScreen = () => {
  const theme = useTheme();
  
  return (
    <MoreStack.Navigator
      screenOptions={{
        headerStyle: {
          backgroundColor: theme.colors.surface,
        },
        headerTintColor: theme.colors.text,
      }}
    >
      <MoreStack.Screen name="More" component={MoreMenuScreen} />
      <MoreStack.Screen name="Whitepaper" component={WhitepaperScreen} />
      <MoreStack.Screen name="Tutorial" component={TutorialScreen} />
    </MoreStack.Navigator>
  );
};

// More menu screen component
const MoreMenuScreen = ({ navigation }: any) => {
  const theme = useTheme();
  
  return (
    <View style={{ flex: 1, backgroundColor: theme.colors.background, padding: 16 }}>
      <TouchableOpacity 
        style={styles.menuItem}
        onPress={() => navigation.navigate('Whitepaper')}
      >
        <Icon name="file-document-outline" size={24} color={theme.colors.primary} />
        <Text style={styles.menuText}>Whitepaper</Text>
      </TouchableOpacity>
      
      <TouchableOpacity 
        style={styles.menuItem}
        onPress={() => navigation.navigate('Tutorial')}
      >
        <Icon name="school-outline" size={24} color={theme.colors.primary} />
        <Text style={styles.menuText}>Tutorial</Text>
      </TouchableOpacity>
    </View>
  );
};

// Main tab navigator
const MainTabNavigator = () => {
  const theme = useTheme();
  
  return (
    <Tab.Navigator
      screenOptions={{
        tabBarActiveTintColor: theme.colors.primary,
        tabBarInactiveTintColor: '#666',
        tabBarStyle: {
          backgroundColor: theme.colors.surface,
          borderTopColor: '#333',
        },
        headerStyle: {
          backgroundColor: theme.colors.surface,
        },
        headerTintColor: theme.colors.text,
      }}
    >
      <Tab.Screen 
        name="Dashboard" 
        component={DashboardScreen} 
        options={{
          tabBarIcon: ({ color }) => <Icon name="view-dashboard" size={24} color={color} />,
        }}
      />
      <Tab.Screen 
        name="Transactions" 
        component={TransactionsScreen} 
        options={{
          tabBarIcon: ({ color }) => <Icon name="swap-horizontal" size={24} color={color} />,
        }}
      />
      <Tab.Screen 
        name="Account" 
        component={AccountScreen} 
        options={{
          tabBarIcon: ({ color }) => <Icon name="wallet" size={24} color={color} />,
        }}
      />
      <Tab.Screen 
        name="SmartContract" 
        component={SmartContractScreen} 
        options={{
          tabBarIcon: ({ color }) => <Icon name="file-code" size={24} color={color} />,
          title: "Smart Contract",
        }}
      />
      <Tab.Screen 
        name="More" 
        component={MoreStackScreen} 
        options={{
          tabBarIcon: ({ color }) => <Icon name="dots-horizontal" size={24} color={color} />,
          headerShown: false,
        }}
      />
    </Tab.Navigator>
  );
};

// Root navigator
const AppNavigator = () => {
  const theme = useTheme();
  
  // Create a custom theme for NavigationContainer
  const navigationTheme = {
    ...DefaultTheme,
    colors: {
      ...DefaultTheme.colors,
      background: theme.colors.background,
      card: theme.colors.surface,
      text: theme.colors.text,
      primary: theme.colors.primary,
    },
  };
  
  return (
    <NavigationContainer theme={navigationTheme}>
      <Stack.Navigator
        screenOptions={{
          headerStyle: {
            backgroundColor: theme.colors.surface,
          },
          headerTintColor: theme.colors.text,
        }}
      >
        <Stack.Screen 
          name="Main" 
          component={MainTabNavigator} 
          options={{ headerShown: false }}
        />
        <Stack.Screen 
          name="ProjectDetails" 
          component={ProjectDetailsScreen} 
          options={{ title: "Project Details" }}
        />
        <Stack.Screen 
          name="MilestoneDetails" 
          component={MilestoneDetailsScreen} 
          options={{ title: "Milestone Details" }}
        />
        <Stack.Screen 
          name="TransactionDetails" 
          component={TransactionDetailsScreen} 
          options={{ title: "Transaction Details" }}
        />
      </Stack.Navigator>
    </NavigationContainer>
  );
};

// Styles
import { StyleSheet, TouchableOpacity, View, Text } from 'react-native';
const styles = StyleSheet.create({
  menuItem: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#1E1E1E',
    padding: 16,
    borderRadius: 8,
    marginBottom: 12,
  },
  menuText: {
    color: '#FFFFFF',
    marginLeft: 16,
    fontSize: 16,
  },
});

export default AppNavigator;