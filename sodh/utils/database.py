import sqlite3
from pathlib import Path
import os

def init_db():
    """Initialize the SQLite database for the application.
    
    Creates the database file and necessary tables if they don't exist.
    """
    # Create the database directory if it doesn't exist
    db_dir = Path('data')
    db_dir.mkdir(exist_ok=True)
    
    # Path to the SQLite database file
    db_path = db_dir / 'sodh.db'
    
    # Connect to the SQLite database (creates it if it doesn't exist)
    conn = sqlite3.connect(str(db_path))
    cursor = conn.cursor()
    
    # Create tables if they don't exist
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS transactions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        signature TEXT NOT NULL,
        slot INTEGER NOT NULL,
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
        status TEXT NOT NULL,
        fee INTEGER,
        data TEXT,
        UNIQUE(signature)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS accounts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        address TEXT NOT NULL,
        balance INTEGER,
        last_updated DATETIME DEFAULT CURRENT_TIMESTAMP,
        metadata TEXT,
        UNIQUE(address)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS config (
        key TEXT PRIMARY KEY,
        value TEXT
    )
    ''')
    
    # Create indexes for better query performance
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_transactions_slot ON transactions(slot)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_transactions_timestamp ON transactions(timestamp)')
    cursor.execute('CREATE INDEX IF NOT EXISTS idx_accounts_address ON accounts(address)')
    
    # Commit changes and close the connection
    conn.commit()
    conn.close()
    
    return str(db_path)
