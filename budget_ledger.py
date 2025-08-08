#!/usr/bin/env python3
"""
Budget Ledger Tool
A simple calculator/ledger for personal finance tracking
"""

import datetime
import json
from typing import Dict, List


class BudgetLedger:
    """Main class for budget and ledger operations"""
    
    def __init__(self):
        self.transactions = []
        self.categories = {
            'income': ['salary', 'freelance', 'investments', 'other'],
            'expenses': ['housing', 'food', 'transport', 'utilities', 'entertainment', 'other'],
            'savings': ['emergency', 'retirement', 'goals'],
            'investments': ['stocks', 'bonds', 'crypto', 'real_estate']
        }
    
    def add_transaction(self, amount: float, category: str, subcategory: str, description: str = ""):
        """Add a new transaction to the ledger"""
        transaction = {
            'date': datetime.datetime.now().isoformat(),
            'amount': amount,
            'category': category,
            'subcategory': subcategory,
            'description': description
        }
        self.transactions.append(transaction)
        return transaction


if __name__ == "__main__":
    print("Budget Ledger Tool - v0.1")
    ledger = BudgetLedger()