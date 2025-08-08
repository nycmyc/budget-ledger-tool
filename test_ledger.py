#!/usr/bin/env python3
"""Test script to populate ledger with sample data"""

from budget_ledger import BudgetLedger
import random
from datetime import datetime, timedelta

def populate_test_data():
    ledger = BudgetLedger("test_ledger.json")
    
    # Add some test transactions
    test_data = [
        (5000, 'income', 'salary', 'Monthly salary'),
        (1200, 'expenses', 'housing', 'Rent payment'),
        (400, 'expenses', 'food', 'Groceries'),
        (150, 'expenses', 'utilities', 'Electric & Internet'),
        (500, 'savings', 'emergency', 'Emergency fund'),
        (1000, 'investments', 'stocks', 'Index fund purchase'),
    ]
    
    for amount, cat, subcat, desc in test_data:
        ledger.add_transaction(amount, cat, subcat, desc)
    
    print(f"Added {len(test_data)} test transactions")
    print(f"Current balance: ${ledger.get_balance():.2f}")

if __name__ == "__main__":
    populate_test_data()