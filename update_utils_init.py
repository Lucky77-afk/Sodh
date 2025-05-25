# Script to update the __init__.py file in the utils directory
init_content = '''# Import utility functions to make them available when importing from sodh.utils
from .database import init_db
from .solana_client_fixed import get_solana_client

__all__ = [
    'init_db',
    'get_solana_client'
]'''

with open('sodh/utils/__init__.py', 'w') as f:
    f.write(init_content)
