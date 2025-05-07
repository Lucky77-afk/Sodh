import { Connection, PublicKey, clusterApiUrl } from '@solana/web3.js';
import solanaService from '../solana-service';

// Mock @solana/web3.js
jest.mock('@solana/web3.js', () => ({
  Connection: jest.fn(),
  PublicKey: jest.fn(),
  clusterApiUrl: jest.fn(),
}));

describe('SolanaService', () => {
  const mockConnection = {
    getBalance: jest.fn(),
    getSignaturesForAddress: jest.fn(),
    getTransaction: jest.fn(),
    getVersion: jest.fn(),
    getSlot: jest.fn(),
    getBlockTime: jest.fn(),
  };

  beforeEach(() => {
    jest.clearAllMocks();
    (Connection as jest.Mock).mockImplementation(() => mockConnection);
    (clusterApiUrl as jest.Mock).mockReturnValue('https://api.devnet.solana.com');
  });

  describe('getBalance', () => {
    it('returns balance in SOL', async () => {
      const mockPublicKey = 'mockPublicKey123';
      const mockBalance = 1000000000; // 1 SOL in lamports
      
      mockConnection.getBalance.mockResolvedValue(mockBalance);

      const balance = await solanaService.getBalance(mockPublicKey);

      expect(Connection).toHaveBeenCalledWith('https://api.devnet.solana.com');
      expect(mockConnection.getBalance).toHaveBeenCalledWith(expect.any(PublicKey));
      expect(balance).toBe(1); // 1 SOL
    });

    it('handles errors', async () => {
      const mockPublicKey = 'mockPublicKey123';
      mockConnection.getBalance.mockRejectedValue(new Error('Network error'));

      await expect(solanaService.getBalance(mockPublicKey)).rejects.toThrow('Network error');
    });
  });

  describe('getTransactionHistory', () => {
    it('returns transaction history', async () => {
      const mockPublicKey = 'mockPublicKey123';
      const mockTransactions = [
        {
          signature: 'tx1',
          slot: 1,
          blockTime: 1234567890,
          status: 'success',
          fee: 0.000005,
        },
      ];

      mockConnection.getSignaturesForAddress.mockResolvedValue(mockTransactions);

      const transactions = await solanaService.getTransactionHistory(mockPublicKey);

      expect(Connection).toHaveBeenCalledWith('https://api.devnet.solana.com');
      expect(mockConnection.getSignaturesForAddress).toHaveBeenCalledWith(
        expect.any(PublicKey),
        { limit: 20 }
      );
      expect(transactions).toEqual(mockTransactions);
    });

    it('handles errors', async () => {
      const mockPublicKey = 'mockPublicKey123';
      mockConnection.getSignaturesForAddress.mockRejectedValue(new Error('Network error'));

      await expect(solanaService.getTransactionHistory(mockPublicKey)).rejects.toThrow('Network error');
    });
  });

  describe('getTransactionDetails', () => {
    it('returns transaction details', async () => {
      const mockSignature = 'tx1';
      const mockTransaction = {
        signature: 'tx1',
        slot: 1,
        blockTime: 1234567890,
        status: 'success',
        fee: 0.000005,
      };

      mockConnection.getTransaction.mockResolvedValue(mockTransaction);

      const transaction = await solanaService.getTransactionDetails(mockSignature);

      expect(Connection).toHaveBeenCalledWith('https://api.devnet.solana.com');
      expect(mockConnection.getTransaction).toHaveBeenCalledWith(mockSignature);
      expect(transaction).toEqual(mockTransaction);
    });

    it('handles errors', async () => {
      const mockSignature = 'tx1';
      mockConnection.getTransaction.mockRejectedValue(new Error('Network error'));

      await expect(solanaService.getTransactionDetails(mockSignature)).rejects.toThrow('Network error');
    });
  });

  describe('getNetworkStatus', () => {
    it('returns network status', async () => {
      const mockVersion = { 'solana-core': '1.0.0' };
      const mockSlot = 12345;
      const mockBlockTime = 1234567890;

      mockConnection.getVersion.mockResolvedValue(mockVersion);
      mockConnection.getSlot.mockResolvedValue(mockSlot);
      mockConnection.getBlockTime.mockResolvedValue(mockBlockTime);

      const status = await solanaService.getNetworkStatus();

      expect(Connection).toHaveBeenCalledWith('https://api.devnet.solana.com');
      expect(mockConnection.getVersion).toHaveBeenCalled();
      expect(mockConnection.getSlot).toHaveBeenCalled();
      expect(mockConnection.getBlockTime).toHaveBeenCalledWith(mockSlot);
      expect(status).toEqual({
        version: mockVersion['solana-core'],
        slot: mockSlot,
        blockTime: mockBlockTime,
      });
    });

    it('handles errors', async () => {
      mockConnection.getVersion.mockRejectedValue(new Error('Network error'));

      await expect(solanaService.getNetworkStatus()).rejects.toThrow('Network error');
    });
  });

  describe('changeNetwork', () => {
    it('changes network successfully', () => {
      solanaService.changeNetwork('mainnet-beta');

      expect(clusterApiUrl).toHaveBeenCalledWith('mainnet-beta');
      expect(Connection).toHaveBeenCalledWith('https://api.mainnet-beta.solana.com');
    });

    it('throws error for invalid network', () => {
      expect(() => {
        solanaService.changeNetwork('invalid-network' as any);
      }).toThrow('Invalid network');
    });
  });
}); 