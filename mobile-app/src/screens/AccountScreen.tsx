import React, { useState, useEffect } from 'react';
import { View, StyleSheet, ScrollView, TouchableOpacity, ActivityIndicator, Alert } from 'react-native';
import { Text, Card, Button, TextInput, useTheme, Divider, List, IconButton } from 'react-native-paper';
import { useUniversalWallet, WalletType } from '../context/UniversalWalletProvider';
import Icon from 'react-native-vector-icons/MaterialCommunityIcons';

type AccountScreenProps = {};

const AccountScreen: React.FC<AccountScreenProps> = () => {
  const theme = useTheme();
  const { 
    address, 
    balance, 
    connected,
    walletType,
    connectWallet, 
    disconnectWallet,
    openWalletApp,
    refreshBalance,
    deepLinkConnect,
    pasteFromClipboard
  } = useUniversalWallet();
  
  const [newAddress, setNewAddress] = useState<string>('');
  const [isLoading, setIsLoading] = useState<boolean>(false);
  
  // Handle connect wallet
  const handleConnect = async () => {
    if (!newAddress) {
      Alert.alert('Error', 'Please enter a wallet address');
      return;
    }
    
    setIsLoading(true);
    try {
      await connectWallet(newAddress);
    } catch (error) {
      Alert.alert('Connection Error', 'Failed to connect wallet');
    } finally {
      setIsLoading(false);
      setNewAddress('');
    }
  };
  
  // Handle clipboard paste
  const handlePaste = async () => {
    const clipboardContent = await pasteFromClipboard();
    setNewAddress(clipboardContent);
  };
  
  // Handle selecting a wallet type
  const handleSelectWalletType = () => {
    Alert.alert(
      'Select Wallet Type',
      'Choose your wallet app',
      [
        { text: 'Phantom', onPress: () => connectWallet(address || newAddress, WalletType.PHANTOM) },
        { text: 'Solflare', onPress: () => connectWallet(address || newAddress, WalletType.SOLFLARE) },
        { text: 'Trust Wallet', onPress: () => connectWallet(address || newAddress, WalletType.TRUSTWALLET) },
        { text: 'Binance', onPress: () => connectWallet(address || newAddress, WalletType.BINANCE) },
        { text: 'CoinDCX', onPress: () => connectWallet(address || newAddress, WalletType.COINDCX) },
        { text: 'Slope', onPress: () => connectWallet(address || newAddress, WalletType.SLOPE) },
        { text: 'Custom', onPress: () => connectWallet(address || newAddress, WalletType.CUSTOM) },
        { text: 'Cancel', style: 'cancel' }
      ]
    );
  };

  if (isLoading) {
    return (
      <View style={[styles.container, styles.centered]}>
        <ActivityIndicator size="large" color={theme.colors.primary} />
        <Text style={{ color: theme.colors.text, marginTop: 16 }}>Connecting wallet...</Text>
      </View>
    );
  }

  return (
    <ScrollView style={[styles.container, { backgroundColor: theme.colors.background }]}>
      {!connected ? (
        <Card style={styles.card}>
          <Card.Title title="Connect Your Wallet" />
          <Card.Content>
            <Text style={[styles.subtitle, { color: theme.colors.text }]}>
              Enter your Solana wallet address to explore your account
            </Text>
            
            <View style={styles.inputContainer}>
              <TextInput
                label="Wallet Address"
                value={newAddress}
                onChangeText={setNewAddress}
                mode="outlined"
                style={styles.input}
                placeholder="Enter Solana wallet address"
              />
              <IconButton
                icon="content-paste"
                size={24}
                onPress={handlePaste}
                style={styles.pasteButton}
              />
            </View>
            
            <View style={styles.buttonContainer}>
              <Button 
                mode="contained" 
                onPress={handleConnect}
                style={[styles.button, { backgroundColor: theme.colors.primary }]}
                disabled={!newAddress}
              >
                Connect Wallet
              </Button>
              
              <Button 
                mode="outlined" 
                onPress={deepLinkConnect}
                style={styles.button}
              >
                Connect with App
              </Button>
            </View>
            
            <Divider style={styles.divider} />
            
            <Text style={[styles.subtitle, { color: theme.colors.text, textAlign: 'center' }]}>
              Compatible with all major Solana wallets
            </Text>
            
            <View style={styles.walletLogos}>
              <View style={styles.walletLogo}>
                <Icon name="ghost" size={32} color="#AB9FF2" />
                <Text style={styles.walletName}>Phantom</Text>
              </View>
              <View style={styles.walletLogo}>
                <Icon name="fire" size={32} color="#FE8F44" />
                <Text style={styles.walletName}>Solflare</Text>
              </View>
              <View style={styles.walletLogo}>
                <Icon name="shield-check" size={32} color="#3375BB" />
                <Text style={styles.walletName}>Trust</Text>
              </View>
              <View style={styles.walletLogo}>
                <Icon name="arrow-up-bold" size={32} color="#8F5AE8" />
                <Text style={styles.walletName}>Slope</Text>
              </View>
            </View>
          </Card.Content>
        </Card>
      ) : (
        <>
          <Card style={styles.card}>
            <Card.Content>
              <View style={styles.accountHeader}>
                <View>
                  <Text style={styles.walletTypeLabel}>
                    {walletType || 'CUSTOM'} WALLET
                  </Text>
                  <Text style={styles.addressText} numberOfLines={1} ellipsizeMode="middle">
                    {address}
                  </Text>
                </View>
                <Button 
                  mode="outlined" 
                  onPress={handleSelectWalletType}
                  style={{ borderColor: theme.colors.primary }}
                >
                  Change Type
                </Button>
              </View>
              
              <View style={styles.balanceContainer}>
                <Text style={styles.balanceLabel}>Available Balance</Text>
                <Text style={styles.balanceValue}>{balance.toFixed(6)} SOL</Text>
                <Text style={styles.fiatValue}>
                  ≈ ${(balance * 150).toFixed(2)} USD
                </Text>
              </View>
              
              <View style={styles.actionsContainer}>
                <Button 
                  mode="contained" 
                  onPress={refreshBalance}
                  style={[styles.actionButton, { backgroundColor: theme.colors.primary }]}
                  icon="refresh"
                >
                  Refresh
                </Button>
                
                <Button 
                  mode="contained" 
                  onPress={openWalletApp}
                  style={[styles.actionButton, { backgroundColor: theme.colors.accent }]}
                  icon="external-link"
                >
                  Open Wallet
                </Button>
                
                <Button 
                  mode="outlined" 
                  onPress={disconnectWallet}
                  style={styles.actionButton}
                  icon="logout"
                >
                  Disconnect
                </Button>
              </View>
            </Card.Content>
          </Card>
          
          <Card style={styles.card}>
            <Card.Title title="Token Balances" />
            <Card.Content>
              <View style={styles.tokenListContainer}>
                <View style={[styles.tokenItem, { backgroundColor: theme.colors.surface }]}>
                  <View style={styles.tokenIcon}>
                    <Text style={styles.tokenInitial}>S</Text>
                  </View>
                  <View style={styles.tokenDetails}>
                    <Text style={styles.tokenName}>Solana</Text>
                    <Text style={styles.tokenTicker}>SOL</Text>
                  </View>
                  <View style={styles.tokenValue}>
                    <Text style={styles.tokenBalance}>{balance.toFixed(6)}</Text>
                    <Text style={styles.tokenFiat}>${(balance * 150).toFixed(2)}</Text>
                  </View>
                </View>
                
                <View style={[styles.tokenItem, { backgroundColor: theme.colors.surface }]}>
                  <View style={[styles.tokenIcon, { backgroundColor: '#26A17B' }]}>
                    <Text style={styles.tokenInitial}>U</Text>
                  </View>
                  <View style={styles.tokenDetails}>
                    <Text style={styles.tokenName}>USDT</Text>
                    <Text style={styles.tokenTicker}>SPL Token</Text>
                  </View>
                  <View style={styles.tokenValue}>
                    <Text style={styles.tokenBalance}>0.00</Text>
                    <Text style={styles.tokenFiat}>$0.00</Text>
                  </View>
                </View>
              </View>
              
              <Text style={styles.tokenDisclaimer}>
                Note: This is view-only. To manage tokens, please use your wallet app.
              </Text>
            </Card.Content>
          </Card>
          
          <Card style={styles.card}>
            <Card.Title title="Explorer Links" />
            <Card.Content>
              <List.Item
                title="View on Solana Explorer"
                description="See transactions, tokens, and more"
                left={props => <List.Icon {...props} icon="open-in-new" />}
                onPress={() => {}}
                titleStyle={{ color: theme.colors.text }}
                descriptionStyle={{ color: '#AAA' }}
              />
              <List.Item
                title="View NFTs"
                description="Check your NFT collection"
                left={props => <List.Icon {...props} icon="image" />}
                onPress={() => {}}
                titleStyle={{ color: theme.colors.text }}
                descriptionStyle={{ color: '#AAA' }}
              />
              <List.Item
                title="Transaction History"
                description="View your recent transactions"
                left={props => <List.Icon {...props} icon="history" />}
                onPress={() => {}}
                titleStyle={{ color: theme.colors.text }}
                descriptionStyle={{ color: '#AAA' }}
              />
            </Card.Content>
          </Card>
        </>
      )}
    </ScrollView>
  );
};

const styles = StyleSheet.create({
  container: {
    flex: 1,
    padding: 16,
  },
  centered: {
    justifyContent: 'center',
    alignItems: 'center',
  },
  card: {
    marginBottom: 16,
    elevation: 4,
  },
  subtitle: {
    fontSize: 16,
    marginBottom: 16,
  },
  inputContainer: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 16,
  },
  input: {
    flex: 1,
  },
  pasteButton: {
    marginLeft: 8,
  },
  buttonContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 16,
  },
  button: {
    flex: 1,
    marginHorizontal: 4,
  },
  divider: {
    marginVertical: 16,
  },
  walletLogos: {
    flexDirection: 'row',
    justifyContent: 'space-around',
    marginTop: 16,
  },
  walletLogo: {
    alignItems: 'center',
  },
  walletName: {
    marginTop: 8,
    fontSize: 12,
    color: '#AAA',
  },
  accountHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  walletTypeLabel: {
    fontSize: 12,
    fontWeight: 'bold',
    color: '#14F195',
    marginBottom: 4,
  },
  addressText: {
    fontFamily: 'monospace',
    color: '#FFF',
    fontSize: 14,
    width: 200,
  },
  balanceContainer: {
    backgroundColor: '#1A1A1A',
    borderRadius: 12,
    padding: 20,
    marginBottom: 20,
    alignItems: 'center',
  },
  balanceLabel: {
    color: '#AAA',
    marginBottom: 8,
  },
  balanceValue: {
    fontSize: 28,
    fontWeight: 'bold',
    color: '#14F195',
    marginBottom: 4,
  },
  fiatValue: {
    color: '#AAA',
    fontSize: 16,
  },
  actionsContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    marginBottom: 16,
  },
  actionButton: {
    flex: 1,
    marginHorizontal: 4,
  },
  tokenListContainer: {
    marginBottom: 16,
  },
  tokenItem: {
    flexDirection: 'row',
    alignItems: 'center',
    padding: 12,
    borderRadius: 8,
    marginBottom: 8,
  },
  tokenIcon: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: '#14F195',
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  tokenInitial: {
    color: '#FFF',
    fontWeight: 'bold',
    fontSize: 18,
  },
  tokenDetails: {
    flex: 1,
  },
  tokenName: {
    color: '#FFF',
    fontWeight: 'bold',
    fontSize: 16,
  },
  tokenTicker: {
    color: '#AAA',
    fontSize: 12,
  },
  tokenValue: {
    alignItems: 'flex-end',
  },
  tokenBalance: {
    color: '#FFF',
    fontWeight: 'bold',
    fontSize: 16,
  },
  tokenFiat: {
    color: '#AAA',
    fontSize: 12,
  },
  tokenDisclaimer: {
    color: '#AAA',
    fontSize: 12,
    fontStyle: 'italic',
    textAlign: 'center',
  },
});

export default AccountScreen;