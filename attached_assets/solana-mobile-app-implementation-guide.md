# Solana Mobile App Implementation Guide for Cursor & Replit

This guide provides step-by-step instructions for implementing the Solana blockchain explorer and smart contract interaction platform using Cursor for code editing and Replit for development and testing.

## Setup and Environment Configuration

### 1. Setting Up Replit

1. Create a new Replit project:
   - Go to [Replit](https://replit.com)
   - Click "Create Repl"
   - Select "React Native (Expo)" template
   - Name your project "solana-explorer-mobile"

2. Initialize the project structure:
   ```bash
   npx create-expo-app -t blank
   ```

3. Install dependencies:
   ```bash
   npm install @solana/web3.js @solana/wallet-adapter-react @solana/wallet-adapter-base
   npm install react-native-paper react-navigation/native react-navigation/stack
   npm install @react-native-async-storage/async-storage
   npm install @expo/vector-icons
   ```

### 2. Setting Up Cursor

1. Download and install [Cursor](https://cursor.so/) if you haven't already
2. Clone your Replit repository to your local machine
3. Open the project folder in Cursor
4. Configure TypeScript:
   - Create `tsconfig.json` in the root directory
   - Set up proper TypeScript configuration for React Native

## Project Structure Implementation

Create the following directory structure in your project:

```
solana-explorer-mobile/
├── assets/                 # App icons and images
├── src/
│   ├── components/         # Reusable UI components
│   ├── context/            # React context providers
│   ├── navigation/         # Navigation configuration
│   ├── screens/            # App screens
│   ├── services/           # API services
│   └── utils/              # Utility functions
├── App.tsx                 # Main app component
├── app.json                # Expo configuration
└── package.json            # Dependencies and scripts
```

## Core Implementation Steps

### 1. Solana Service Setup

Create `src/services/solana-service.ts`:

```typescript
import { Connection, clusterApiUrl, PublicKey, Transaction } from '@solana/web3.js';

class SolanaService {
  private connection: Connection;
  
  constructor(network: 'mainnet-beta' | 'testnet' | 'devnet' = 'devnet') {
    this.connection = new Connection(clusterApiUrl(network));
  }
  
  // Get account balance
  async getBalance(publicKey: string): Promise<number> {
    try {
      const pubKey = new PublicKey(publicKey);
      const balance = await this.connection.getBalance(pubKey);
      return balance / 1000000000; // Convert lamports to SOL
    } catch (error) {
      console.error('Error getting balance:', error);
      throw error;
    }
  }
  
  // Get transaction history for an account
  async getTransactionHistory(publicKey: string): Promise<any[]> {
    try {
      const pubKey = new PublicKey(publicKey);
      const transactions = await this.connection.getSignaturesForAddress(pubKey);
      return transactions;
    } catch (error) {
      console.error('Error getting transaction history:', error);
      throw error;
    }
  }
  
  // Get transaction details
  async getTransactionDetails(signature: string): Promise<any> {
    try {
      const transaction = await this.connection.getTransaction(signature);
      return transaction;
    } catch (error) {
      console.error('Error getting transaction details:', error);
      throw error;
    }
  }
  
  // Get network status
  async getNetworkStatus(): Promise<any> {
    try {
      const version = await this.connection.getVersion();
      const slot = await this.connection.getSlot();
      const blockTime = await this.connection.getBlockTime(slot);
      
      return {
        version,
        slot,
        blockTime
      };
    } catch (error) {
      console.error('Error getting network status:', error);
      throw error;
    }
  }
  
  // Change network
  changeNetwork(network: 'mainnet-beta' | 'testnet' | 'devnet'): void {
    this.connection = new Connection(clusterApiUrl(network));
  }
}

export default new SolanaService();
```

### 2. Wallet Context Setup

Create `src/context/WalletContext.tsx`:

```typescript
import React, { createContext, useState, useContext, ReactNode } from 'react';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { PublicKey } from '@solana/web3.js';

interface WalletContextType {
  publicKey: string | null;
  connectWallet: (publicKey: string) => Promise<void>;
  disconnectWallet: () => Promise<void>;
  isConnected: boolean;
}

const WalletContext = createContext<WalletContextType | undefined>(undefined);

export const WalletProvider: React.FC<{ children: ReactNode }> = ({ children }) => {
  const [publicKey, setPublicKey] = useState<string | null>(null);
  const [isConnected, setIsConnected] = useState<boolean>(false);

  // Load saved wallet on initialization
  React.useEffect(() => {
    const loadWallet = async () => {
      try {
        const savedPublicKey = await AsyncStorage.getItem('walletPublicKey');
        if (savedPublicKey) {
          setPublicKey(savedPublicKey);
          setIsConnected(true);
        }
      } catch (error) {
        console.error('Error loading wallet:', error);
      }
    };

    loadWallet();
  }, []);

  const connectWallet = async (publicKeyString: string) => {
    try {
      // Validate that the string is a valid public key
      new PublicKey(publicKeyString);
      
      // Save to state and storage
      setPublicKey(publicKeyString);
      await AsyncStorage.setItem('walletPublicKey', publicKeyString);
      setIsConnected(true);
    } catch (error) {
      console.error('Invalid public key:', error);
      throw new Error('Invalid public key format');
    }
  };

  const disconnectWallet = async () => {
    try {
      setPublicKey(null);
      await AsyncStorage.removeItem('walletPublicKey');
      setIsConnected(false);
    } catch (error) {
      console.error('Error disconnecting wallet:', error);
      throw error;
    }
  };

  return (
    <WalletContext.Provider value={{ publicKey, connectWallet, disconnectWallet, isConnected }}>
      {children}
    </WalletContext.Provider>
  );
};

export const useWallet = () => {
  const context = useContext(WalletContext);
  if (context === undefined) {
    throw new Error('useWallet must be used within a WalletProvider');
  }
  return context;
};
```

### 3. Navigation Setup

Create `src/navigation/AppNavigation.tsx`:

```typescript
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
```

### 4. Key Screen Implementations

#### HomeScreen.tsx

```typescript
import React, { useState, useEffect } from 'react';
import { View, StyleSheet, ScrollView } from 'react-native';
import { Card, Title, Paragraph, Button, ActivityIndicator } from 'react-native-paper';
import { useNavigation } from '@react-navigation/native';
import solanaService from '../services/solana-service';
import { useWallet } from '../context/WalletContext';

const HomeScreen = () => {
  const navigation = useNavigation();
  const { publicKey, isConnected } = useWallet();
  const [networkStatus, setNetworkStatus] = useState<any>(null);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchNetworkStatus = async () => {
      try {
        setLoading(true);
        const status = await solanaService.getNetworkStatus();
        setNetworkStatus(status);
        setError(null);
      } catch (err) {
        setError('Failed to fetch network status');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchNetworkStatus();
    // Refresh every 30 seconds
    const interval = setInterval(fetchNetworkStatus, 30000);
    return () => clearInterval(interval);
  }, []);

  const handleConnectWallet = () => {
    navigation.navigate('ConnectWallet');
  };

  return (
    <ScrollView style={styles.container}>
      {/* Network Status Card */}
      <Card style={styles.card}>
        <Card.Content>
          <Title style={styles.title}>Solana Network Status</Title>
          {loading ? (
            <ActivityIndicator size="small" color="#512DA8" />
          ) : error ? (
            <Paragraph style={styles.error}>{error}</Paragraph>
          ) : (
            <>
              <View style={styles.infoRow}>
                <Paragraph style={styles.label}>Network:</Paragraph>
                <Paragraph style={styles.value}>Devnet</Paragraph>
              </View>
              <View style={styles.infoRow}>
                <Paragraph style={styles.label}>Current Slot:</Paragraph>
                <Paragraph style={styles.value}>{networkStatus?.slot}</Paragraph>
              </View>
              <View style={styles.infoRow}>
                <Paragraph style={styles.label}>Version:</Paragraph>
                <Paragraph style={styles.value}>{networkStatus?.version?.['solana-core']}</Paragraph>
              </View>
            </>
          )}
        </Card.Content>
      </Card>

      {/* Wallet Card */}
      <Card style={styles.card}>
        <Card.Content>
          <Title style={styles.title}>Wallet</Title>
          {isConnected ? (
            <>
              <View style={styles.infoRow}>
                <Paragraph style={styles.label}>Public Key:</Paragraph>
                <Paragraph style={styles.value} numberOfLines={1} ellipsizeMode="middle">
                  {publicKey}
                </Paragraph>
              </View>
              <Button
                mode="contained"
                style={styles.button}
                onPress={() => navigation.navigate('Wallet')}
              >
                View Wallet
              </Button>
            </>
          ) : (
            <>
              <Paragraph style={styles.paragraph}>
                Connect a wallet to view your SOL and tokens.
              </Paragraph>
              <Button mode="contained" style={styles.button} onPress={handleConnectWallet}>
                Connect Wallet
              </Button>
            </>
          )}
        </Card.Content>
      </Card>

      {/* Features Card */}
      <Card style={styles.card}>
        <Card.Content>
          <Title style={styles.title}>Explorer Features</Title>
          <Paragraph style={styles.paragraph}>
            • View real-time blockchain data
          </Paragraph>
          <Paragraph style={styles.paragraph}>
            • Track transaction history
          </Paragraph>
          <Paragraph style={styles.paragraph}>
            • Interact with smart contracts
          </Paragraph>
          <Paragraph style={styles.paragraph}>
            • Manage projects and collaborations
          </Paragraph>
          <Button
            mode="contained"
            style={styles.button}
            onPress={() => navigation.navigate('Explorer')}
          >
            Open Explorer
          </Button>
        </Card.Content>
      </Card>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1E1E1E',
    padding: 16,
  },
  card: {
    marginBottom: 16,
    backgroundColor: '#2C2C2C',
    borderRadius: 8,
  },
  title: {
    color: '#FFFFFF',
    marginBottom: 12,
  },
  paragraph: {
    color: '#E0E0E0',
    marginBottom: 8,
  },
  infoRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 8,
  },
  label: {
    color: '#BDBDBD',
    flex: 1,
  },
  value: {
    color: '#E0E0E0',
    flex: 2,
    textAlign: 'right',
  },
  button: {
    marginTop: 12,
    backgroundColor: '#512DA8',
  },
  error: {
    color: '#F44336',
  },
});

export default HomeScreen;
```

#### ExplorerScreen.tsx

```typescript
import React, { useState } from 'react';
import { View, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import { TextInput, Button, Card, Title, Paragraph, Divider, Chip } from 'react-native-paper';
import { useNavigation } from '@react-navigation/native';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import solanaService from '../services/solana-service';

const ExplorerScreen = () => {
  const navigation = useNavigation();
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [searchType, setSearchType] = useState<'account' | 'transaction'>('account');

  const handleSearch = async () => {
    if (!searchQuery.trim()) {
      setError('Please enter a valid search query');
      return;
    }

    setLoading(true);
    setError(null);
    
    try {
      if (searchType === 'account') {
        // Fetch account info and transactions
        const balance = await solanaService.getBalance(searchQuery);
        const transactions = await solanaService.getTransactionHistory(searchQuery);
        
        setSearchResults({
          type: 'account',
          address: searchQuery,
          balance,
          transactions: transactions.slice(0, 5) // Get first 5 transactions
        });
      } else {
        // Fetch transaction info
        const txInfo = await solanaService.getTransactionDetails(searchQuery);
        setSearchResults({
          type: 'transaction',
          signature: searchQuery,
          details: txInfo
        });
      }
    } catch (err) {
      console.error('Search error:', err);
      setError(`Invalid ${searchType}. Please check and try again.`);
    } finally {
      setLoading(false);
    }
  };

  const renderAccountResults = () => {
    const { address, balance, transactions } = searchResults;
    
    return (
      <Card style={styles.resultCard}>
        <Card.Content>
          <Title style={styles.title}>Account Information</Title>
          <View style={styles.infoRow}>
            <Paragraph style={styles.label}>Address:</Paragraph>
            <Paragraph style={styles.value} numberOfLines={1} ellipsizeMode="middle">
              {address}
            </Paragraph>
          </View>
          <View style={styles.infoRow}>
            <Paragraph style={styles.label}>Balance:</Paragraph>
            <Paragraph style={styles.value}>{balance} SOL</Paragraph>
          </View>
          
          <Divider style={styles.divider} />
          
          <Title style={styles.title}>Recent Transactions</Title>
          {transactions.length > 0 ? (
            transactions.map((tx, index) => (
              <TouchableOpacity
                key={index}
                onPress={() => navigation.navigate('TransactionDetail', { signature: tx.signature })}
              >
                <View style={styles.transactionItem}>
                  <Paragraph style={styles.transactionText} numberOfLines={1} ellipsizeMode="middle">
                    {tx.signature}
                  </Paragraph>
                  <MaterialCommunityIcons name="chevron-right" size={24} color="#BDBDBD" />
                </View>
                {index < transactions.length - 1 && <Divider style={styles.itemDivider} />}
              </TouchableOpacity>
            ))
          ) : (
            <Paragraph style={styles.noDataText}>No transactions found</Paragraph>
          )}
          
          {transactions.length > 0 && (
            <Button 
              mode="text" 
              onPress={() => {}} 
              style={styles.viewAllButton}
            >
              View All Transactions
            </Button>
          )}
        </Card.Content>
      </Card>
    );
  };

  const renderTransactionResults = () => {
    const { signature, details } = searchResults;
    
    if (!details) {
      return (
        <Card style={styles.resultCard}>
          <Card.Content>
            <Title style={styles.title}>Transaction Details</Title>
            <Paragraph style={styles.error}>Transaction not found</Paragraph>
          </Card.Content>
        </Card>
      );
    }
    
    return (
      <Card style={styles.resultCard}>
        <Card.Content>
          <Title style={styles.title}>Transaction Details</Title>
          <View style={styles.infoRow}>
            <Paragraph style={styles.label}>Signature:</Paragraph>
            <Paragraph style={styles.value} numberOfLines={1} ellipsizeMode="middle">
              {signature}
            </Paragraph>
          </View>
          <View style={styles.infoRow}>
            <Paragraph style={styles.label}>Slot:</Paragraph>
            <Paragraph style={styles.value}>{details.slot}</Paragraph>
          </View>
          <View style={styles.infoRow}>
            <Paragraph style={styles.label}>Block Time:</Paragraph>
            <Paragraph style={styles.value}>
              {details.blockTime ? new Date(details.blockTime * 1000).toLocaleString() : 'N/A'}
            </Paragraph>
          </View>
          <View style={styles.infoRow}>
            <Paragraph style={styles.label}>Status:</Paragraph>
            <Chip 
              style={[styles.statusChip, { backgroundColor: details.meta?.err ? '#F44336' : '#4CAF50' }]}
            >
              {details.meta?.err ? 'Failed' : 'Success'}
            </Chip>
          </View>
          
          <Button
            mode="contained"
            style={styles.button}
            onPress={() => navigation.navigate('TransactionDetail', { signature })}
          >
            View Full Details
          </Button>
        </Card.Content>
      </Card>
    );
  };

  return (
    <ScrollView style={styles.container}>
      <Card style={styles.searchCard}>
        <Card.Content>
          <Title style={styles.title}>Solana Explorer</Title>
          
          <View style={styles.searchTypeContainer}>
            <TouchableOpacity
              style={[
                styles.searchTypeButton,
                searchType === 'account' && styles.activeSearchType
              ]}
              onPress={() => setSearchType('account')}
            >
              <Paragraph style={[
                styles.searchTypeText,
                searchType === 'account' && styles.activeSearchTypeText
              ]}>
                Account
              </Paragraph>
            </TouchableOpacity>
            <TouchableOpacity
              style={[
                styles.searchTypeButton,
                searchType === 'transaction' && styles.activeSearchType
              ]}
              onPress={() => setSearchType('transaction')}
            >
              <Paragraph style={[
                styles.searchTypeText,
                searchType === 'transaction' && styles.activeSearchTypeText
              ]}>
                Transaction
              </Paragraph>
            </TouchableOpacity>
          </View>
          
          <TextInput
            label={`Enter ${searchType} address`}
            value={searchQuery}
            onChangeText={setSearchQuery}
            style={styles.searchInput}
            theme={{ colors: { primary: '#512DA8' } }}
          />
          
          {error && <Paragraph style={styles.error}>{error}</Paragraph>}
          
          <Button
            mode="contained"
            onPress={handleSearch}
            loading={loading}
            disabled={loading}
            style={styles.button}
          >
            Search
          </Button>
        </Card.Content>
      </Card>

      {searchResults && (
        searchResults.type === 'account' ? renderAccountResults() : renderTransactionResults()
      )}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1E1E1E',
    padding: 16,
  },
  searchCard: {
    marginBottom: 16,
    backgroundColor: '#2C2C2C',
    borderRadius: 8,
  },
  resultCard: {
    backgroundColor: '#2C2C2C',
    borderRadius: 8,
    marginBottom: 16,
  },
  title: {
    color: '#FFFFFF',
    marginBottom: 12,
  },
  searchTypeContainer: {
    flexDirection: 'row',
    marginBottom: 16,
  },
  searchTypeButton: {
    flex: 1,
    paddingVertical: 8,
    alignItems: 'center',
    borderBottomWidth: 2,
    borderBottomColor: 'transparent',
  },
  activeSearchType: {
    borderBottomColor: '#512DA8',
  },
  searchTypeText: {
    color: '#BDBDBD',
  },
  activeSearchTypeText: {
    color: '#FFFFFF',
  },
  searchInput: {
    backgroundColor: '#3C3C3C',
    marginBottom: 12,
  },
  button: {
    marginTop: 12,
    backgroundColor: '#512DA8',
  },
  viewAllButton: {
    marginTop: 8,
    alignSelf: 'center',
  },
  error: {
    color: '#F44336',
    marginTop: 8,
  },
  infoRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  label: {
    color: '#BDBDBD',
    flex: 1,
  },
  value: {
    color: '#E0E0E0',
    flex: 2,
    textAlign: 'right',
  },
  divider: {
    backgroundColor: '#424242',
    height: 1,
    marginVertical: 16,
  },
  itemDivider: {
    backgroundColor: '#424242',
    height: 1,
    marginVertical: 8,
  },
  transactionItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 8,
  },
  transactionText: {
    color: '#E0E0E0',
    flex: 1,
  },
  noDataText: {
    color: '#BDBDBD',
    fontStyle: 'italic',
    textAlign: 'center',
    marginVertical: 8,
  },
  statusChip: {
    height: 24,
    justifyContent: 'center',
  },
});

export default ExplorerScreen;
```

### 5. App Entry Point

Update `App.tsx`:

```typescript
import React from 'react';
import { StatusBar } from 'expo-status-bar';
import { SafeAreaProvider } from 'react-native-safe-area-context';
import { Provider as PaperProvider, DefaultTheme } from 'react-native-paper';
import AppNavigation from './src/navigation/AppNavigation';
import { WalletProvider } from './src/context/WalletContext';

const theme = {
  ...DefaultTheme,
  colors: {
    ...DefaultTheme.colors,
    primary: '#512DA8',
    accent: '#7C4DFF',
    background: '#1E1E1E',
    surface: '#2C2C2C',
    text: '#FFFFFF',
  },
};

export default function App() {
  return (
    <SafeAreaProvider>
      <PaperProvider theme={theme}>
        <WalletProvider>
          <StatusBar style="light" />
          <AppNavigation />
        </WalletProvider>
      </PaperProvider>
    </SafeAreaProvider>
  );
}
```

## Testing in Replit

1. Push your changes to Replit
2. In the Replit shell, run:
   ```bash
   npm start
   ```
3. Scan the QR code with the Expo Go app on your mobile device
4. Test the app functionality

## Smart Contract Interaction Implementation

To implement smart contract interaction, add this functionality:

### 1. Create Smart Contract Service

Create `src/services/contract-service.ts`:

```typescript
import { Connection, PublicKey, Transaction, TransactionInstruction } from '@solana/web3.js';
import { Buffer } from 'buffer';

class ContractService {
  private connection: Connection;
  
  constructor(endpoint: string) {
    this.connection = new Connection(endpoint);
  }
  
  // Get program accounts
  async getProgramAccounts(programId: string): Promise<any[]> {
    try {
      const pubKey = new PublicKey(programId);
      const accounts = await this.connection.getProgramAccounts(pubKey);
      return accounts.map(account => ({
        pubkey: account.pubkey.toString(),
        account: {
          data: account.account.data,
          executable: account.account.executable,
          lamports: account.account.lamports,
          owner: account.account.owner.toString(),
        }
      }));
    } catch (error) {
      console.error('Error getting program accounts:', error);
      throw error;
    }
  }
  
  // Parse contract data (simplified example)
  parseContractData(data: Buffer): any {
    // This is a placeholder - actual parsing depends on the specific contract format
    try {
      // For demonstration, returning a generic object
      return {
        rawData: data.toString('hex'),
        dataLength: data.length,
      };
    } catch (error) {
      console.error('Error parsing contract data:', error);
      throw error;
    }
  }
  
  // Get program info
  async getProgramInfo(programId: string): Promise<any> {
    try {
      const pubKey = new PublicKey(programId);
      const accountInfo = await this.connection.getAccountInfo(pubKey);
      return {
        executable: accountInfo?.executable,
        lamports: accountInfo?.lamports,
        owner: accountInfo?.owner.toString(),
        dataLength: accountInfo?.data.length,
      };
    } catch (error) {
      console.error('Error getting program info:', error);
      throw error;
    }
  }
}

export default new ContractService('https://api.devnet.solana.com');
```

### 2. Create Contract Explorer Screen

Create `src/screens/ContractExplorerScreen.tsx`:

```typescript
import React, { useState } from 'react';
import { View, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import { TextInput, Button, Card, Title, Paragraph, Divider, List, ActivityIndicator } from 'react-native-paper';
import { useNavigation } from '@react-navigation/native';
import contractService from '../services/contract-service';

const ContractExplorerScreen = () => {
  const navigation = useNavigation();
  const [programId, setProgramId] = useState('');
  const [programInfo, setProgramInfo] = useState<any>(null);
  const [accounts, setAccounts] = useState<any[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [expandedAccount, setExpandedAccount] = useState<string | null>(null);

  const handleExplore = async () => {
    if (!programId.trim()) {
      setError('Please enter a valid program ID');
      return;
    }

    setLoading(true);
    setError(null);
    setProgramInfo(null);
    setAccounts([]);
    
    try {
      // Get program info
      const info = await contractService.getProgramInfo(programId);
      setProgramInfo(info);
      
      // Get program accounts
      const programAccounts = await contractService.getProgramAccounts(programId);
      setAccounts(programAccounts);
    } catch (err) {
      console.error('Contract exploration error:', err);
      setError('Invalid program ID or network error. Please check and try again.');
    } finally {
      setLoading(false);
    }
  };

  const toggleAccountExpansion = (pubkey: string) => {
    if (expandedAccount === pubkey) {
      setExpandedAccount(null);
    } else {
      setExpandedAccount(pubkey);
    }
  };

  const renderProgramInfo = () => {
    if (!programInfo) return null;
    
    return (
      <Card style={styles.card}>
        <Card.Content>
          <Title style={styles.title}>Program Information</Title>
          <View style={styles.infoRow}>
            <Paragraph style={styles.label}>Program ID:</Paragraph>
            <Paragraph style={styles.value} numberOfLines={1} ellipsizeMode="middle">
              {programId}
            </Paragraph>
          </View>
          <View style={styles.infoRow}>
            <Paragraph style={styles.label}>Executable:</Paragraph>
            <Paragraph style={styles.value}>
              {programInfo.executable ? 'Yes' : 'No'}
            </Paragraph>
          </View>
          <View style={styles.infoRow}>
            <Paragraph style={styles.label}>Balance:</Paragraph>
            <Paragraph style={styles.value}>
              {programInfo.lamports / 1000000000} SOL
            </Paragraph>
          </View>
          <View style={styles.infoRow}>
            <Paragraph style={styles.label}>Owner:</Paragraph>
            <Paragraph style={styles.value} numberOfLines={1} ellipsizeMode="middle">
              {programInfo.owner}
            </Paragraph>
          </View>
          <View style={styles.infoRow}>
            <Paragraph style={styles.label}>Data Size:</Paragraph>
            <Paragraph style={styles.value}>
              {programInfo.dataLength} bytes
            </Paragraph>
          </View>
        </Card.Content>
      </Card>
    );
  };

  const renderAccounts = () => {
    if (accounts.length === 0) return null;
    
    return (
      <Card style={styles.card}>
        <Card.Content>
          <Title style={styles.title}>Program Accounts ({accounts.length})</Title>
          
          {accounts.map((account, index) => (
            <View key={account.pubkey}>
              <TouchableOpacity onPress={() => toggleAccountExpansion(account.pubkey)}>
                <View style={styles.accountItem}>
                  <Paragraph style={styles.accountTitle} numberOfLines={1} ellipsizeMode="middle">
                    {account.pubkey}
                  </Paragraph>
                  <Paragraph style={styles.accountBalance}>
                    {account.account.lamports / 1000000000} SOL
                  </Paragraph>
                </View>
              </TouchableOpacity>
              
              {expandedAccount === account.pubkey && (
                <View style={styles.expandedAccount}>
                  <View style={styles.accountDetailRow}>
                    <Paragraph style={styles.detailLabel}>Owner:</Paragraph>
                    <Paragraph style={styles.detailValue} numberOfLines={1} ellipsizeMode="middle">
                      {account.account.owner}
                    </Paragraph>
                  </View>
                  <View style={styles.accountDetailRow}>
                    <Paragraph style={styles.detailLabel}>Data Size:</Paragraph>
                    <Paragraph style={styles.detailValue}>
                      {Buffer.isBuffer(account.account.data) ? account.account.data.length : 'N/A'} bytes
                    </Paragraph>
                  </View>
                  <View style={styles.accountDetailRow}>
                    <Paragraph style={styles.detailLabel}>Executable:</Paragraph>
                    <Paragraph style={styles.detailValue}>
                      {account.account.executable ? 'Yes' : 'No'}
                    </Paragraph>
                  </View>
                  
                  <Button 
                    mode="outlined" 
                    style={styles.dataButton}
                    onPress={() => navigation.navigate('AccountDataScreen', { 
                      pubkey: account.pubkey,
                      data: Buffer.isBuffer(account.account.data) 
                        ? account.account.data.toString('hex') 
                        : JSON.stringify(account.account.data)
                    })}
                  >
                    View Data
                  </Button>
                </View>
              )}
              
              {index < accounts.length - 1 && <Divider style={styles.divider} />}
            </View>
          ))}
        </Card.Content>
      </Card>
    );
  };

  return (
    <ScrollView style={styles.container}>
      <Card style={styles.searchCard}>
        <Card.Content>
          <Title style={styles.title}>Smart Contract Explorer</Title>
          <Paragraph style={styles.subtitle}>
            Enter a Solana program ID to explore its accounts and data
          </Paragraph>
          
          <TextInput
            label="Program ID"
            value={programId}
            onChangeText={setProgramId}
            style={styles.input}
            theme={{ colors: { primary: '#512DA8' } }}
          />
          
          {error && <Paragraph style={styles.error}>{error}</Paragraph>}
          
          <Button
            mode="contained"
            onPress={handleExplore}
            loading={loading}
            disabled={loading}
            style={styles.button}
          >
            Explore Program
          </Button>
        </Card.Content>
      </Card>

      {loading && (
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color="#512DA8" />
          <Paragraph style={styles.loadingText}>Loading program data...</Paragraph>
        </View>
      )}

      {!loading && programInfo && renderProgramInfo()}
      {!loading && accounts.length > 0 && renderAccounts()}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1E1E1E',
    padding: 16,
  },
  searchCard: {
    marginBottom: 16,
    backgroundColor: '#2C2C2C',
    borderRadius: 8,
  },
  card: {
    backgroundColor: '#2C2C2C',
    borderRadius: 8,
    marginBottom: 16,
  },
  title: {
    color: '#FFFFFF',
    marginBottom: 8,
  },
  subtitle: {
    color: '#BDBDBD',
    marginBottom: 16,
  },
  input: {
    backgroundColor: '#3C3C3C',
    marginBottom: 12,
  },
  button: {
    marginTop: 12,
    backgroundColor: '#512DA8',
  },
  error: {
    color: '#F44336',
    marginTop: 8,
  },
  loadingContainer: {
    alignItems: 'center',
    padding: 24,
  },
  loadingText: {
    color: '#BDBDBD',
    marginTop: 12,
  },
  infoRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  label: {
    color: '#BDBDBD',
    flex: 1,
  },
  value: {
    color: '#E0E0E0',
    flex: 2,
    textAlign: 'right',
  },
  divider: {
    backgroundColor: '#424242',
    height: 1,
    marginVertical: 8,
  },
  accountItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 8,
  },
  accountTitle: {
    color: '#E0E0E0',
    flex: 3,
  },
  accountBalance: {
    color: '#81C784',
    flex: 1,
    textAlign: 'right',
  },
  expandedAccount: {
    backgroundColor: '#3C3C3C',
    padding: 12,
    borderRadius: 4,
    marginVertical: 8,
  },
  accountDetailRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 8,
  },
  detailLabel: {
    color: '#BDBDBD',
    flex: 1,
  },
  detailValue: {
    color: '#E0E0E0',
    flex: 2,
  },
  dataButton: {
    marginTop: 8,
    borderColor: '#7C4DFF',
  },
});

export default ContractExplorerScreen;



AccountDataScreen 

import React, { useState } from 'react';
import { View, StyleSheet, ScrollView } from 'react-native';
import { Card, Title, Paragraph, Chip, Button, Divider, Subheading } from 'react-native-paper';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import * as Clipboard from 'expo-clipboard';

// Define the route params interface
interface RouteParams {
  pubkey: string;
  data: string;
}

const AccountDataScreen = ({ route }) => {
  const { pubkey, data } = route.params as RouteParams;
  const [copied, setCopied] = useState(false);
  const [viewMode, setViewMode] = useState<'hex' | 'utf8'>('hex');
  
  // Format data for display
  const formatHexData = (hexString: string) => {
    // Group hex by pairs and add spaces
    return hexString.match(/.{1,2}/g)?.join(' ') || hexString;
  };
  
  const getUtf8Data = (hexString: string) => {
    try {
      // Convert hex to UTF-8 string
      const bytes = Buffer.from(hexString, 'hex');
      return bytes.toString('utf8').replace(/\0/g, ' '); // Replace null bytes with spaces
    } catch (error) {
      return '[Data cannot be displayed as UTF-8]';
    }
  };
  
  const displayData = viewMode === 'hex' 
    ? formatHexData(data) 
    : getUtf8Data(data);
  
  const copyToClipboard = async () => {
    await Clipboard.setStringAsync(data);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };
  
  return (
    <ScrollView style={styles.container}>
      <Card style={styles.card}>
        <Card.Content>
          <Title style={styles.title}>Account Data</Title>
          <Paragraph style={styles.subtitle} numberOfLines={1} ellipsizeMode="middle">
            {pubkey}
          </Paragraph>
          
          <View style={styles.infoRow}>
            <Paragraph style={styles.label}>Size:</Paragraph>
            <Paragraph style={styles.value}>{Math.floor(data.length / 2)} bytes</Paragraph>
          </View>
          
          <View style={styles.actions}>
            <Button 
              icon="content-copy" 
              mode="outlined" 
              onPress={copyToClipboard}
              style={styles.copyButton}
            >
              {copied ? 'Copied!' : 'Copy Data'}
            </Button>
            
            <View style={styles.viewModeContainer}>
              <Chip 
                selected={viewMode === 'hex'} 
                onPress={() => setViewMode('hex')}
                style={styles.chip}
                selectedColor="#FFFFFF"
              >
                Hex
              </Chip>
              <Chip 
                selected={viewMode === 'utf8'} 
                onPress={() => setViewMode('utf8')}
                style={styles.chip}
                selectedColor="#FFFFFF"
              >
                UTF-8
              </Chip>
            </View>
          </View>
          
          <Divider style={styles.divider} />
          
          <Subheading style={styles.dataTitle}>
            Raw Data ({viewMode.toUpperCase()})
          </Subheading>
          
          <View style={styles.dataContainer}>
            <ScrollView horizontal={true} style={styles.horizontalScroll}>
              <Paragraph style={styles.dataText}>
                {displayData}
              </Paragraph>
            </ScrollView>
          </View>
          
          <View style={styles.infoBox}>
            <MaterialCommunityIcons name="information-outline" size={20} color="#64B5F6" />
            <Paragraph style={styles.infoText}>
              Data interpretation depends on the program's specific data structure. 
              This is the raw account data in {viewMode === 'hex' ? 'hexadecimal' : 'UTF-8'} format.
            </Paragraph>
          </View>
        </Card.Content>
      </Card>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1E1E1E',
    padding: 16,
  },
  card: {
    backgroundColor: '#2C2C2C',
    borderRadius: 8,
  },
  title: {
    color: '#FFFFFF',
    marginBottom: 4,
  },
  subtitle: {
    color: '#BDBDBD',
    marginBottom: 16,
  },
  infoRow: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 8,
  },
  label: {
    color: '#BDBDBD',
    flex: 1,
  },
  value: {
    color: '#E0E0E0',
    flex: 2,
    textAlign: 'right',
  },
  actions: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginVertical: 12,
  },
  copyButton: {
    borderColor: '#7C4DFF',
  },
  viewModeContainer: {
    flexDirection: 'row',
  },
  chip: {
    marginLeft: 8,
    backgroundColor: '#3C3C3C',
  },
  divider: {
    backgroundColor: '#424242',
    height: 1,
    marginVertical: 16,
  },
  dataTitle: {
    color: '#E0E0E0',
    marginBottom: 12,
  },
  dataContainer: {
    backgroundColor: '#212121',
    borderRadius: 4,
    padding: 12,
    marginBottom: 16,
  },
  horizontalScroll: {
    maxHeight: 300,
  },
  dataText: {
    color: '#E0E0E0',
    fontFamily: 'monospace',
    fontSize: 12,
    lineHeight: 20,
  },
  infoBox: {
    flexDirection: 'row',
    backgroundColor: 'rgba(100, 181, 246, 0.1)',
    borderRadius: 4,
    padding: 12,
  },
  infoText: {
    color: '#E0E0E0',
    marginLeft: 8,
    flex: 1,
  },
});

export default AccountDataScreen;

implementing the WalletScreen and ConnectWalletScreen which are essential for the Solana mobile app. These screens will allow users to connect their wallets (view-only) and see their balances and transactions.

import React, { useState, useEffect } from 'react';
import { View, StyleSheet, ScrollView, RefreshControl, TouchableOpacity } from 'react-native';
import { Card, Title, Paragraph, Button, ActivityIndicator, Divider, Avatar } from 'react-native-paper';
import { useNavigation } from '@react-navigation/native';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import * as Clipboard from 'expo-clipboard';

import { useWallet } from '../context/WalletContext';
import solanaService from '../services/solana-service';

const WalletScreen = () => {
  const navigation = useNavigation();
  const { publicKey, disconnectWallet, isConnected } = useWallet();
  
  const [balance, setBalance] = useState<number | null>(null);
  const [transactions, setTransactions] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [copied, setCopied] = useState(false);
  const [error, setError] = useState<string | null>(null);

  // Fetch wallet data
  const fetchWalletData = async () => {
    if (!publicKey) return;
    
    try {
      setError(null);
      // Get SOL balance
      const balanceValue = await solanaService.getBalance(publicKey);
      setBalance(balanceValue);
      
      // Get recent transactions
      const txHistory = await solanaService.getTransactionHistory(publicKey);
      setTransactions(txHistory.slice(0, 10)); // Get first 10 transactions
    } catch (err) {
      console.error('Error fetching wallet data:', err);
      setError('Failed to fetch wallet data. Please try again.');
    } finally {
      setLoading(false);
      setRefreshing(false);
    }
  };

  // Initial data loading
  useEffect(() => {
    if (isConnected) {
      fetchWalletData();
    } else {
      setLoading(false);
    }
  }, [isConnected, publicKey]);

  // Handle refresh
  const onRefresh = () => {
    setRefreshing(true);
    fetchWalletData();
  };

  // Handle wallet disconnect
  const handleDisconnect = async () => {
    try {
      await disconnectWallet();
      navigation.navigate('Home');
    } catch (err) {
      console.error('Error disconnecting wallet:', err);
    }
  };

  // Copy address to clipboard
  const copyAddressToClipboard = async () => {
    if (publicKey) {
      await Clipboard.setStringAsync(publicKey);
      setCopied(true);
      setTimeout(() => setCopied(false), 2000);
    }
  };

  // Render content based on connection state
  if (!isConnected) {
    return (
      <View style={styles.container}>
        <Card style={styles.card}>
          <Card.Content style={styles.centerContent}>
            <Avatar.Icon 
              size={80} 
              icon="wallet-outline" 
              style={styles.walletIcon} 
              color="#FFFFFF" 
            />
            <Title style={styles.title}>No Wallet Connected</Title>
            <Paragraph style={styles.paragraph}>
              Connect a wallet to view your balances and transactions
            </Paragraph>
            <Button 
              mode="contained" 
              style={styles.button}
              onPress={() => navigation.navigate('ConnectWallet')}
            >
              Connect Wallet
            </Button>
          </Card.Content>
        </Card>
      </View>
    );
  }

  return (
    <ScrollView 
      style={styles.container}
      refreshControl={
        <RefreshControl refreshing={refreshing} onRefresh={onRefresh} colors={['#512DA8']} />
      }
    >
      {/* Wallet Address Card */}
      <Card style={styles.card}>
        <Card.Content>
          <View style={styles.addressHeader}>
            <Title style={styles.title}>Wallet</Title>
            <Button 
              mode="text" 
              compact 
              onPress={handleDisconnect}
              style={styles.disconnectButton}
            >
              Disconnect
            </Button>
          </View>
          
          <View style={styles.addressContainer}>
            <Paragraph style={styles.addressLabel}>Address:</Paragraph>
            <TouchableOpacity 
              style={styles.addressValue} 
              onPress={copyAddressToClipboard}
            >
              <Paragraph style={styles.addressText} numberOfLines={1} ellipsizeMode="middle">
                {publicKey}
              </Paragraph>
              <MaterialCommunityIcons 
                name={copied ? "check" : "content-copy"} 
                size={16} 
                color={copied ? "#4CAF50" : "#BDBDBD"} 
              />
            </TouchableOpacity>
          </View>
        </Card.Content>
      </Card>

      {/* Balance Card */}
      <Card style={styles.card}>
        <Card.Content>
          <Title style={styles.title}>Balance</Title>
          {loading ? (
            <ActivityIndicator size="small" color="#512DA8" style={styles.loader} />
          ) : error ? (
            <Paragraph style={styles.error}>{error}</Paragraph>
          ) : (
            <View style={styles.balanceContainer}>
              <View style={styles.tokenBalance}>
                <Avatar.Icon 
                  size={40} 
                  icon="currency-sign" 
                  style={styles.tokenIcon} 
                  color="#FFFFFF" 
                />
                <View style={styles.tokenInfo}>
                  <Paragraph style={styles.tokenName}>SOL</Paragraph>
                  <Title style={styles.tokenValue}>
                    {balance !== null ? balance.toFixed(4) : '0.0000'}
                  </Title>
                </View>
              </View>
            </View>
          )}
        </Card.Content>
      </Card>

      {/* Transaction History Card */}
      <Card style={styles.card}>
        <Card.Content>
          <Title style={styles.title}>Recent Transactions</Title>
          
          {loading ? (
            <ActivityIndicator size="small" color="#512DA8" style={styles.loader} />
          ) : error ? (
            <Paragraph style={styles.error}>{error}</Paragraph>
          ) : transactions.length > 0 ? (
            transactions.map((tx, index) => (
              <View key={index}>
                <TouchableOpacity
                  onPress={() => navigation.navigate('TransactionDetail', { signature: tx.signature })}
                >
                  <View style={styles.transactionItem}>
                    <View style={styles.transactionLeft}>
                      <MaterialCommunityIcons 
                        name="swap-horizontal" 
                        size={24} 
                        color="#7C4DFF" 
                      />
                      <View style={styles.transactionInfo}>
                        <Paragraph style={styles.transactionLabel}>
                          Transaction
                        </Paragraph>
                        <Paragraph style={styles.transactionValue} numberOfLines={1} ellipsizeMode="middle">
                          {tx.signature}
                        </Paragraph>
                      </View>
                    </View>
                    <MaterialCommunityIcons name="chevron-right" size={24} color="#BDBDBD" />
                  </View>
                </TouchableOpacity>
                {index < transactions.length - 1 && <Divider style={styles.divider} />}
              </View>
            ))
          ) : (
            <Paragraph style={styles.emptyMessage}>No transactions found</Paragraph>
          )}
          
          {transactions.length > 0 && (
            <Button 
              mode="text" 
              onPress={() => navigation.navigate('TransactionHistory', { address: publicKey })}
              style={styles.viewAllButton}
            >
              View All Transactions
            </Button>
          )}
        </Card.Content>
      </Card>
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: '#1E1E1E',
    padding: 16,
  },
  card: {
    marginBottom: 16,
    backgroundColor: '#2C2C2C',
    borderRadius: 8,
  },
  centerContent: {
    alignItems: 'center',
    padding: 24,
  },
  walletIcon: {
    backgroundColor: '#512DA8',
    marginBottom: 16,
  },
  title: {
    color: '#FFFFFF',
    marginBottom: 12,
  },
  paragraph: {
    color: '#E0E0E0',
    marginBottom: 24,
    textAlign: 'center',
  },
  button: {
    marginTop: 12,
    backgroundColor: '#512DA8',
    width: '80%',
  },
  addressHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 12,
  },
  disconnectButton: {
    margin: 0,
    padding: 0,
  },
  addressContainer: {
    marginBottom: 8,
  },
  addressLabel: {
    color: '#BDBDBD',
    marginBottom: 4,
  },
  addressValue: {
    flexDirection: 'row',
    alignItems: 'center',
    backgroundColor: '#3C3C3C',
    borderRadius: 4,
    padding: 8,
  },
  addressText: {
    color: '#E0E0E0',
    flex: 1,
    marginRight: 8,
    fontFamily: 'monospace',
  },
  balanceContainer: {
    marginTop: 8,
  },
  tokenBalance: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 16,
  },
  tokenIcon: {
    backgroundColor: '#512DA8',
    marginRight: 16,
  },
  tokenInfo: {
    flex: 1,
  },
  tokenName: {
    color: '#BDBDBD',
  },
  tokenValue: {
    color: '#FFFFFF',
  },
  loader: {
    marginVertical: 16,
  },
  error: {
    color: '#F44336',
    marginVertical: 16,
  },
  divider: {
    backgroundColor: '#424242',
    height: 1,
    marginVertical: 12,
  },
  transactionItem: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    paddingVertical: 12,
  },
  transactionLeft: {
    flexDirection: 'row',
    alignItems: 'center',
    flex: 1,
  },
  transactionInfo: {
    marginLeft: 12,
    flex: 1,
  },
  transactionLabel: {
    color: '#BDBDBD',
    fontSize: 12,
  },
  transactionValue: {
    color: '#E0E0E0',
  },
  emptyMessage: {
    color: '#BDBDBD',
    fontStyle: 'italic',
    textAlign: 'center',
    marginVertical: 16,
  },
  viewAllButton: {
    marginTop: 8,
  },
});

export default WalletScreen;

 ConnectWalletScreen

import React, { useState } from 'react';
import { View, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import { TextInput, Button, Card, Title, Paragraph, Avatar, Dialog, Portal } from 'react-native-paper';
import { useNavigation } from '@react-navigation/native';
import { MaterialCommunityIcons } from '@expo/vector-icons';
import { PublicKey } from '@solana/web3.js';

import { useWallet } from '../context/WalletContext';

const ConnectWalletScreen = () => {
  const navigation = useNavigation();
  const { connectWallet } = useWallet();
  
  const [publicKeyInput, setPublicKeyInput] = useState('');
  const [error, setError] = useState<string | null>(