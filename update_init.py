# Script to update the __init__.py file in the components directory
init_content = """# Import all component functions to make them available when importing from sodh.components
from .header import render_header
from .dashboard_fixed import render_dashboard
from .transactions_simple import render_transactions
from .account_fixed import render_account
from .smart_contract import render_smart_contract
from .whitepaper_fixed import render_whitepaper
from .tutorial_simple import render_tutorial

__all__ = [
    'render_header',
    'render_dashboard',
    'render_transactions',
    'render_account',
    'render_smart_contract',
    'render_whitepaper',
    'render_tutorial'
]"""

with open('sodh/components/__init__.py', 'w') as f:
    f.write(init_content)
