use anchor_lang::prelude::*;
use anchor_spl::token::{self, Token, TokenAccount, Transfer};

declare_id!("DAPPRCo11abC0llab111111111111111111111111111111");

#[program]
pub mod dappr_collab {
    use super::*;

    // Initialize a new collaboration agreement
    pub fn initialize_agreement(
        ctx: Context<InitializeAgreement>,
        title: String,
        description: String,
    ) -> Result<()> {
        let agreement = &mut ctx.accounts.agreement;
        let clock = Clock::get()?;
        
        agreement.creator = *ctx.accounts.creator.key;
        agreement.title = title;
        agreement.description = description;
        agreement.created_at = clock.unix_timestamp;
        agreement.is_active = true;
        
        // Add creator as initial participant
        agreement.participants.push(Participant {
            pubkey: *ctx.accounts.creator.key,
            is_admin: true,
        });
        
        emit!(AgreementCreated {
            agreement: agreement.key(),
            creator: agreement.creator,
            timestamp: clock.unix_timestamp,
        });
        
        Ok(())
    }

    // Add a new milestone to the agreement
    pub fn add_milestone(
        ctx: Context<UpdateAgreement>,
        description: String,
        due_date: i64,
        amount: u64,
    ) -> Result<()> {
        let agreement = &mut ctx.accounts.agreement;
        
        // Simple check for admin
        require!(
            agreement.participants.iter().any(|p| p.pubkey == *ctx.accounts.creator.key && p.is_admin),
            ErrorCode::Unauthorized
        );
        
        let milestone = Milestone {
            description,
            due_date,
            amount,
            is_completed: false,
            is_paid: false,
            recipient: *ctx.accounts.creator.key, // Default to creator, can be updated
        };
        
        agreement.milestones.push(milestone);
        
        emit!(MilestoneAdded {
            agreement: agreement.key(),
            milestone_index: agreement.milestones.len() - 1,
            timestamp: Clock::get()?.unix_timestamp,
        });
        
        Ok(())
    }

    // Complete a milestone
    pub fn complete_milestone(
        ctx: Context<UpdateMilestone>,
        milestone_index: u8,
    ) -> Result<()> {
        let agreement = &mut ctx.accounts.agreement;
        
        // Only admin can mark as completed
        require!(
            agreement.participants.iter().any(|p| p.pubkey == *ctx.accounts.creator.key && p.is_admin),
            ErrorCode::Unauthorized
        );
        
        require!(
            (milestone_index as usize) < agreement.milestones.len(),
            ErrorCode::InvalidMilestoneIndex
        );
        
        let milestone = &mut agreement.milestones[milestone_index as usize];
        milestone.is_completed = true;
        
        emit!(MilestoneCompleted {
            agreement: agreement.key(),
            milestone_index: milestone_index as u64,
            timestamp: Clock::get()?.unix_timestamp,
        });
        
        Ok(())
    }

    // Release payment for a milestone
    pub fn release_payment(
        ctx: Context<ReleasePayment>,
        milestone_index: u8,
    ) -> Result<()> {
        let agreement = &mut ctx.accounts.agreement;
        
        // Only admin can release payment
        require!(
            agreement.participants.iter().any(|p| p.pubkey == *ctx.accounts.creator.key && p.is_admin),
            ErrorCode::Unauthorized
        );
        
        require!(
            (milestone_index as usize) < agreement.milestones.len(),
            ErrorCode::InvalidMilestoneIndex
        );
        
        let milestone = &mut agreement.milestones[milestone_index as usize];
        
        require!(
            milestone.is_completed && !milestone.is_paid,
            ErrorCode::InvalidMilestoneStatus
        );
        
        // Transfer tokens from vault to recipient
        let transfer_ctx = CpiContext::new(
            ctx.accounts.token_program.to_account_info(),
            Transfer {
                from: ctx.accounts.vault.to_account_info(),
                to: ctx.accounts.recipient_token_account.to_account_info(),
                authority: ctx.accounts.authority.to_account_info(),
            },
        );
        
        token::transfer(transfer_ctx, milestone.amount)?;
        
        milestone.is_paid = true;
        
        emit!(PaymentReleased {
            agreement: agreement.key(),
            milestone_index: milestone_index as u64,
            amount: milestone.amount,
            recipient: milestone.recipient,
            timestamp: Clock::get()?.unix_timestamp,
        });
        
        Ok(())
    }
    
    // Add funds to the agreement vault
    pub fn fund_vault(
        ctx: Context<FundVault>,
        amount: u64,
    ) -> Result<()> {
        let transfer_ctx = CpiContext::new(
            ctx.accounts.token_program.to_account_info(),
            Transfer {
                from: ctx.accounts.from.to_account_info(),
                to: ctx.accounts.vault.to_account_info(),
                authority: ctx.accounts.owner.to_account_info(),
            },
        );
        
        token::transfer(transfer_ctx, amount)?;
        
        emit!(VaultFunded {
            vault: ctx.accounts.vault.key(),
            amount,
            timestamp: Clock::get()?.unix_timestamp,
        });
        
        Ok(())
    }
}

// Account Structures
#[account]
pub struct Agreement {
    pub creator: Pubkey,
    pub title: String,
    pub description: String,
    pub created_at: i64,
    pub is_active: bool,
    pub participants: Vec<Participant>,
    pub milestones: Vec<Milestone>,
}

#[derive(AnchorSerialize, AnchorDeserialize, Clone)]
pub struct Participant {
    pub pubkey: Pubkey,
    pub is_admin: bool,
}

#[derive(AnchorSerialize, AnchorDeserialize, Clone)]
pub struct Milestone {
    pub description: String,
    pub due_date: i64,
    pub amount: u64,
    pub is_completed: bool,
    pub is_paid: bool,
    pub recipient: Pubkey,
}

// Contexts
#[derive(Accounts)]
pub struct InitializeAgreement<'info> {
    #[account(init, payer = creator, space = 8 + 32 + 100 + 500 + 8 + 1 + 4 + (32 + 1) * 10 + 4 + (100 + 8 + 8 + 1 + 1 + 32) * 10)]
    pub agreement: Account<'info, Agreement>,
    #[account(mut)]
    pub creator: Signer<'info>,
    pub system_program: Program<'info, System>,
}

#[derive(Accounts)]
pub struct UpdateAgreement<'info> {
    #[account(mut)]
    pub agreement: Account<'info, Agreement>,
    pub creator: Signer<'info>,
}

#[derive(Accounts)]
pub struct UpdateMilestone<'info> {
    #[account(mut)]
    pub agreement: Account<'info, Agreement>,
    pub creator: Signer<'info>,
}

#[derive(Accounts)]
pub struct ReleasePayment<'info> {
    #[account(mut)]
    pub agreement: Account<'info, Agreement>,
    #[account(mut)]
    pub vault: Account<'info, TokenAccount>,
    #[account(mut)]
    pub recipient_token_account: Account<'info, TokenAccount>,
    pub authority: Signer<'info>,
    pub token_program: Program<'info, Token>,
    pub creator: Signer<'info>,
}

#[derive(Accounts)]
pub struct FundVault<'info> {
    #[account(mut)]
    pub vault: Account<'info, TokenAccount>,
    #[account(mut)]
    pub from: Account<'info, TokenAccount>,
    pub owner: Signer<'info>,
    pub token_program: Program<'info, Token>,
}

// Events
#[event]
pub struct AgreementCreated {
    pub agreement: Pubkey,
    pub creator: Pubkey,
    pub timestamp: i64,
}

#[event]
pub struct MilestoneAdded {
    pub agreement: Pubkey,
    pub milestone_index: u64,
    pub timestamp: i64,
}

#[event]
pub struct MilestoneCompleted {
    pub agreement: Pubkey,
    pub milestone_index: u64,
    pub timestamp: i64,
}

#[event]
pub struct PaymentReleased {
    pub agreement: Pubkey,
    pub milestone_index: u64,
    pub amount: u64,
    pub recipient: Pubkey,
    pub timestamp: i64,
}

#[event]
pub struct VaultFunded {
    pub vault: Pubkey,
    pub amount: u64,
    pub timestamp: i64,
}

// Error Codes
#[error_code]
pub enum ErrorCode {
    #[msg("Invalid milestone index")]
    InvalidMilestoneIndex,
    #[msg("Invalid milestone status")]
    InvalidMilestoneStatus,
    #[msg("Unauthorized")]
    Unauthorized,
}
