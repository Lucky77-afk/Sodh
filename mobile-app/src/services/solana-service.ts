import { Connection, PublicKey } from '@solana/web3.js';

// Constants
const SYSTEM_PROGRAM_ID = "11111111111111111111111111111111";
const TOKEN_PROGRAM_ID = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA";
const USDT_MINT = "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB"; // USDT on Solana

/**
 * Get recent blocks from the Solana blockchain
 * @param connection Solana connection instance
 * @param limit Number of blocks to fetch
 * @returns Array of recent blocks
 */
export const getRecentBlocks = async (connection: Connection, limit: number = 10) => {
  try {
    // Get recent confirmed blocks
    const blocks = await connection.getRecentBlockhash();
    const slot = await connection.getSlot();
    
    // Get block time information
    const blockTime = await connection.getBlockTime(slot);
    
    // For mobile, we'll simulate multiple blocks since the API
    // doesn't directly provide a list of recent blocks
    const recentBlocks = [];
    
    // Add the latest block
    recentBlocks.push({
      slot,
      blockhash: blocks.blockhash,
      timestamp: blockTime || Math.floor(Date.now() / 1000)
    });
    
    // Simulate older blocks for UI demonstration
    for (let i = 1; i < limit; i++) {
      recentBlocks.push({
        slot: slot - i,
        blockhash: `sim${blocks.blockhash.substring(3)}${i}`,
        timestamp: (blockTime || Math.floor(Date.now() / 1000)) - (i * 2)
      });
    }
    
    return recentBlocks;
  } catch (error) {
    console.error('Error fetching recent blocks:', error);
    throw error;
  }
};

/**
 * Get recent transactions from the Solana blockchain
 * @param connection Solana connection instance
 * @param limit Number of transactions to fetch
 * @returns Array of recent transactions
 */
export const getRecentTransactions = async (connection: Connection, limit: number = 10) => {
  try {
    // Get recent confirmed signatures for System Program (which gets many transactions)
    const signatures = await connection.getSignaturesForAddress(
      new PublicKey(SYSTEM_PROGRAM_ID),
      { limit }
    );
    
    const transactions = [];
    
    // Process each signature to get transaction details
    for (const sigInfo of signatures) {
      const signature = sigInfo.signature;
      
      // Get transaction details
      const tx = await connection.getTransaction(signature);
      
      if (!tx) continue;
      
      // Determine transaction status
      const status = tx.meta?.err ? "Failed" : "Success";
      
      // Get block time
      const blockTime = tx.blockTime 
        ? new Date(tx.blockTime * 1000).toLocaleString()
        : "Unknown";
      
      // Try to determine transaction type
      let txType = "Unknown";
      
      try {
        // Simple heuristic for transaction type based on the first instruction's program ID
        const firstInstruction = tx.transaction.message.instructions[0];
        
        if (firstInstruction) {
          const programId = tx.transaction.message.accountKeys[firstInstruction.programIndex].toString();
          
          // Map program IDs to transaction types
          const programMap: Record<string, string> = {
            "11111111111111111111111111111111": "Transfer",
            "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA": "Token",
            "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL": "Associated Token",
            "Stake11111111111111111111111111111111111111": "Stake",
            "9xQeWvG816bUx9EPjHmaT23yvVM2ZWbrrpZb9PusVFin": "Serum DEX",
          };
          
          txType = programMap[programId] || "Other";
        }
      } catch (e) {
        console.warn('Error determining transaction type:', e);
      }
      
      // Calculate fee in SOL
      const fee = (tx.meta?.fee || 0) / 1_000_000_000; // Convert lamports to SOL
      
      transactions.push({
        signature,
        status,
        block_time: blockTime,
        slot: tx.slot,
        fee,
        type: txType
      });
    }
    
    return transactions;
  } catch (error) {
    console.error('Error fetching recent transactions:', error);
    throw error;
  }
};

/**
 * Get detailed information for a specific transaction
 * @param connection Solana connection instance
 * @param signature Transaction signature
 * @returns Transaction details or null
 */
export const getTransactionDetails = async (connection: Connection, signature: string) => {
  try {
    const tx = await connection.getTransaction(signature);
    return tx;
  } catch (error) {
    console.error('Error fetching transaction details:', error);
    throw error;
  }
};

/**
 * Get account information and balances
 * @param connection Solana connection instance
 * @param address Wallet address
 * @returns Account information
 */
export const getAccountInfo = async (connection: Connection, address: string) => {
  try {
    // Check if the address is valid
    if (!address || address.length < 32) {
      throw new Error('Invalid address format');
    }
    
    const publicKey = new PublicKey(address);
    
    // Get SOL balance
    const balance = await connection.getBalance(publicKey);
    const balanceSol = balance / 1_000_000_000; // Convert lamports to SOL
    
    // Get transaction count
    const signatures = await connection.getSignaturesForAddress(publicKey, { limit: 100 });
    const txCount = signatures.length;
    
    // Try to get USDT token balance
    let usdtBalance = 0;
    
    try {
      // Find USDT associated token account for this wallet
      const tokenAccounts = await connection.getTokenAccountsByOwner(
        publicKey,
        { mint: new PublicKey(USDT_MINT) }
      );
      
      if (tokenAccounts.value.length > 0) {
        // Get token account info for the first matching account
        const tokenAccountPubkey = tokenAccounts.value[0].pubkey;
        const tokenAccountInfo = await connection.getTokenAccountBalance(tokenAccountPubkey);
        
        // Extract USDT balance
        usdtBalance = tokenAccountInfo.value.uiAmount || 0;
      }
    } catch (e) {
      console.warn('Error fetching token balances:', e);
    }
    
    // Current market values (would come from price API in production)
    const solPriceUsd = 150.00;
    
    return {
      address,
      balance_sol: balanceSol,
      balance_usdt: usdtBalance,
      transaction_count: txCount,
      creation_time: Math.floor(Date.now() / 1000) - (3600 * 24 * 30), // Placeholder
      tokens: [
        { symbol: 'SOL', balance: balanceSol, usd_value: balanceSol * solPriceUsd },
        { symbol: 'USDT', balance: usdtBalance, usd_value: usdtBalance },
      ]
    };
  } catch (error) {
    console.error('Error fetching account info:', error);
    throw error;
  }
};

/**
 * Get recent transactions for a specific account
 * @param connection Solana connection instance
 * @param address Wallet address
 * @param limit Number of transactions to fetch
 * @returns Array of account transactions
 */
export const getAccountTransactions = async (connection: Connection, address: string, limit: number = 5) => {
  try {
    // Check if address is valid
    if (!address || address.length < 32) {
      throw new Error('Invalid address format');
    }
    
    const publicKey = new PublicKey(address);
    
    // Get recent signatures for this account
    const signatures = await connection.getSignaturesForAddress(publicKey, { limit });
    
    const transactions = [];
    
    // Process each transaction
    for (const sigInfo of signatures) {
      const signature = sigInfo.signature;
      
      // Get transaction details
      const tx = await connection.getTransaction(signature);
      
      if (!tx) continue;
      
      // Determine transaction status
      const status = tx.meta?.err === null;
      
      // Get block time and slot
      const blockTime = tx.blockTime || 0;
      const slot = tx.slot;
      
      // Try to determine transaction amount and direction
      let amount = 0;
      let txType = "Unknown";
      
      try {
        // Check transaction message
        const accountKeys = tx.transaction.message.accountKeys;
        const instructions = tx.transaction.message.instructions;
        
        if (instructions.length > 0) {
          const firstInst = instructions[0];
          const programId = accountKeys[firstInst.programIndex].toString();
          
          // Handle System Program transfers (SOL)
          if (programId === SYSTEM_PROGRAM_ID) {
            txType = "Transfer";
            
            // Determine if sending or receiving
            if (accountKeys[0].toString() === address) {
              txType = "Send";
            } else {
              txType = "Receive";
            }
            
            // Calculate amount from pre/post balances
            if (tx.meta?.preBalances && tx.meta?.postBalances) {
              const balanceDiff = Math.abs(tx.meta.postBalances[0] - tx.meta.preBalances[0]);
              amount = balanceDiff / 1_000_000_000; // Convert lamports to SOL
            }
          } 
          // Handle Token Program transfers (SPL tokens)
          else if (programId === TOKEN_PROGRAM_ID) {
            txType = "Token";
          }
          // Handle Stake Program
          else if (programId === "Stake11111111111111111111111111111111111111") {
            txType = "Stake";
          }
        }
      } catch (e) {
        console.warn('Error parsing transaction data:', e);
      }
      
      transactions.push({
        signature,
        status,
        blockTime,
        slot,
        amount,
        type: txType
      });
    }
    
    return transactions;
  } catch (error) {
    console.error('Error fetching account transactions:', error);
    throw error;
  }
};

/**
 * Get projects from our custom program
 * This would connect to our smart contract in a real implementation
 */
export const getProjects = async (connection: Connection) => {
  // In a real app, this would query your smart contract
  // For demo purposes, we'll return mock data
  return [
    {
      id: "proj1",
      name: "Quantum Computing Algorithm",
      description: "Collaborative research on quantum computing algorithms for protein folding prediction",
      status: "Active",
      participants: 4,
      milestones: 3,
      created_at: "2025-04-01",
    },
    {
      id: "proj2",
      name: "Neural Interface Design",
      description: "Development of non-invasive neural interfaces for medical applications",
      status: "Active",
      participants: 6,
      milestones: 5,
      created_at: "2025-03-15",
    },
    {
      id: "proj3",
      name: "Sustainable Energy Storage",
      description: "Research on high-capacity renewable energy storage technologies",
      status: "Pending",
      participants: 3,
      milestones: 2,
      created_at: "2025-04-10",
    }
  ];
};

/**
 * Get milestones for a specific project
 * This would connect to our smart contract in a real implementation
 */
export const getMilestones = async (connection: Connection, projectId: string) => {
  // In a real app, this would query your smart contract
  // For demo purposes, we'll return mock data
  return [
    {
      id: "mile1",
      projectId,
      title: "Initial Quantum Algorithm Design",
      description: "Develop theoretical framework for quantum algorithms targeting protein folding predictions",
      deadline: "2025-05-23",
      payment: "50 USDT",
      status: "Funded"
    },
    {
      id: "mile2",
      projectId,
      title: "Prototype Implementation",
      description: "Implement prototype of quantum algorithm on simulator and analyze performance",
      deadline: "2025-06-23",
      payment: "1.5 SOL",
      status: "Pending"
    },
    {
      id: "mile3",
      projectId,
      title: "Final Report & Optimization",
      description: "Optimize algorithm for specific hardware and prepare final documentation",
      deadline: "2025-07-15",
      payment: "75 USDT",
      status: "Pending"
    }
  ];
};