import * as anchor from "@project-serum/anchor";
import { Program } from "@project-serum/anchor";
import { DapprCollab } from "../target/types/dappr_collab";
import { PublicKey, SystemProgram, SYSVAR_RENT_PUBKEY, Keypair } from "@solana/web3.js";
import { TOKEN_PROGRAM_ID, createMint, getOrCreateAssociatedTokenAccount, mintTo, createAssociatedTokenAccount } from "@solana/spl-token";

describe("DAPPR Collaboration Agreement MVP", () => {
  // Configure the client to use the local cluster.
  const provider = anchor.AnchorProvider.env();
  anchor.setProvider(provider);
  const program = anchor.workspace.DapprCollab as Program<DapprCollab>;

  // Generate a new keypair for the agreement
  const agreement = Keypair.generate();
  
  // Test token mint (simulating USDC)
  let testMint: PublicKey;
  
  // Test accounts
  let creatorTokenAccount: PublicKey;
  let vaultTokenAccount: PublicKey;
  let recipientTokenAccount: PublicKey;
  let recipientWallet: Keypair;

  before(async () => {
    // Create a test token mint
    testMint = await createMint(
      provider.connection,
      provider.wallet.payer,
      provider.wallet.publicKey,
      null,
      6 // Decimals
    );

    // Create token accounts for testing
    creatorTokenAccount = await getOrCreateAssociatedTokenAccount(
      provider.connection,
      provider.wallet.payer,
      testMint,
      provider.wallet.publicKey
    );

    // Create a recipient wallet
    recipientWallet = Keypair.generate();
    
    // Create recipient token account
    recipientTokenAccount = await getOrCreateAssociatedTokenAccount(
      provider.connection,
      provider.wallet.payer,
      testMint,
      recipientWallet.publicKey
    );

    // Create vault token account (owned by the program)
    const [vaultAuth] = await PublicKey.findProgramAddress(
      [Buffer.from("vault"), agreement.publicKey.toBuffer()],
      program.programId
    );
    
    vaultTokenAccount = await createAssociatedTokenAccount(
      provider.connection,
      provider.wallet.payer,
      testMint,
      vaultAuth,
      true // Allow owner off curve
    );

    // Mint test tokens to creator
    await mintTo(
      provider.connection,
      provider.wallet.payer,
      testMint,
      creatorTokenAccount.address,
      provider.wallet.payer,
      1_000_000_000 // 1000 tokens (6 decimals)
    );
  });

  it("Initialize Agreement", async () => {
    // Initialize the agreement
    await program.methods.initializeAgreement(
      "Test Agreement",
      "This is a test collaboration agreement"
    )
    .accounts({
      agreement: agreement.publicKey,
      creator: provider.wallet.publicKey,
      systemProgram: SystemProgram.programId,
    })
    .signers([agreement])
    .rpc();

    // Verify the agreement was created
    const agreementAccount = await program.account.agreement.fetch(agreement.publicKey);
    console.log("Agreement created:", agreementAccount.title);
  });

  it("Add Milestone", async () => {
    const dueDate = Math.floor(Date.now() / 1000) + 30 * 24 * 60 * 60; // 30 days from now
    
    await program.methods.addMilestone(
      "Complete MVP",
      new anchor.BN(dueDate),
      new anchor.BN(100 * 1e6) // 100 tokens
    )
    .accounts({
      agreement: agreement.publicKey,
      creator: provider.wallet.publicKey,
    })
    .rpc();

    // Verify the milestone was added
    const agreementAccount = await program.account.agreement.fetch(agreement.publicKey);
    console.log("Milestone added:", agreementAccount.milestones[0].description);
  });

  it("Fund Vault", async () => {
    await program.methods.fundVault(
      new anchor.BN(500 * 1e6) // 500 tokens
    )
    .accounts({
      vault: vaultTokenAccount,
      from: creatorTokenAccount.address,
      owner: provider.wallet.publicKey,
      tokenProgram: TOKEN_PROGRAM_ID,
    })
    .rpc();

    console.log("Vault funded successfully");
  });

  it("Complete Milestone", async () => {
    await program.methods.completeMilestone(0)
      .accounts({
        agreement: agreement.publicKey,
        creator: provider.wallet.publicKey,
      })
      .rpc();

    console.log("Milestone marked as completed");
  });

  it("Release Payment", async () => {
    await program.methods.releasePayment(0)
      .accounts({
        agreement: agreement.publicKey,
        vault: vaultTokenAccount,
        recipientTokenAccount: recipientTokenAccount.address,
        authority: provider.wallet.publicKey,
        tokenProgram: TOKEN_PROGRAM_ID,
        creator: provider.wallet.publicKey,
      })
      .rpc();

    console.log("Payment released successfully");
  });

  it("Verify Final State", async () => {
    const agreementAccount = await program.account.agreement.fetch(agreement.publicKey);
    const milestone = agreementAccount.milestones[0];
    
    console.log("Milestone status:", {
      description: milestone.description,
      isCompleted: milestone.isCompleted,
      isPaid: milestone.isPaid,
      amount: milestone.amount.toString(),
      recipient: milestone.recipient.toString()
    });
    
    // Verify the milestone is marked as paid
    const assert = require('assert');
    assert(milestone.isPaid, "Milestone should be marked as paid");
  });
});
