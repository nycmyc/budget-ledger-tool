#!/usr/bin/env python3
"""
Budget Ledger Tool
A simple calculator/ledger for personal finance tracking
"""

import datetime
import json
from typing import Dict, List
from pathlib import Path


class BudgetLedger:
    """Main class for budget and ledger operations"""
    
    def __init__(self, data_file: str = "ledger_data.json"):
        self.data_file = Path(data_file)
        self.transactions = []
        self.categories = {
            'income': ['salary', 'freelance', 'investments', 'other'],
            'expenses': ['housing', 'food', 'transport', 'utilities', 'entertainment', 'other'],
            'savings': ['emergency', 'retirement', 'goals'],
            'investments': ['stocks', 'bonds', 'crypto', 'real_estate']
        }
        self.load_data()
    
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
        self.save_data()
        return transaction
    
    def get_balance(self) -> float:
        """Calculate current balance (income - expenses)"""
        income = sum(t['amount'] for t in self.transactions if t['category'] == 'income')
        expenses = sum(t['amount'] for t in self.transactions if t['category'] == 'expenses')
        return income - expenses
    
    def get_monthly_summary(self, year: int, month: int) -> Dict:
        """Get summary for a specific month"""
        monthly_transactions = [
            t for t in self.transactions
            if datetime.datetime.fromisoformat(t['date']).year == year
            and datetime.datetime.fromisoformat(t['date']).month == month
        ]
        
        summary = {
            'income': sum(t['amount'] for t in monthly_transactions if t['category'] == 'income'),
            'expenses': sum(t['amount'] for t in monthly_transactions if t['category'] == 'expenses'),
            'savings': sum(t['amount'] for t in monthly_transactions if t['category'] == 'savings'),
            'investments': sum(t['amount'] for t in monthly_transactions if t['category'] == 'investments')
        }
        summary['net'] = summary['income'] - summary['expenses']
        summary['savings_rate'] = (summary['savings'] / summary['income'] * 100) if summary['income'] > 0 else 0
        
        return summary
    
    def save_data(self):
        """Save transactions to JSON file"""
        with open(self.data_file, 'w') as f:
            json.dump(self.transactions, f, indent=2)
    
    def load_data(self):
        """Load transactions from JSON file"""
        if self.data_file.exists():
            with open(self.data_file, 'r') as f:
                self.transactions = json.load(f)


def main():
    """Main CLI interface"""
    ledger = BudgetLedger()
    
    while True:
        print("\n=== Budget Ledger Tool ===")
        print(f"Current Balance: ${ledger.get_balance():.2f}")
        print("\n1. Add Income")
        print("2. Add Expense")
        print("3. Add Savings")
        print("4. Add Investment")
        print("5. View Monthly Summary")
        print("6. Exit")
        
        choice = input("\nSelect option: ")
        
        if choice == '6':
            break
        elif choice in ['1', '2', '3', '4']:
            category_map = {'1': 'income', '2': 'expenses', '3': 'savings', '4': 'investments'}
            category = category_map[choice]
            
            amount = float(input("Amount: $"))
            print(f"Subcategories: {', '.join(ledger.categories[category])}")
            subcategory = input("Subcategory: ")
            description = input("Description (optional): ")
            
            ledger.add_transaction(amount, category, subcategory, description)
            print(f"✓ Transaction added!")
        
        elif choice == '5':
            year = int(input("Year (YYYY): "))
            month = int(input("Month (1-12): "))
            summary = ledger.get_monthly_summary(year, month)
            
            print(f"\n--- Summary for {month}/{year} ---")
            print(f"Income: ${summary['income']:.2f}")
            print(f"Expenses: ${summary['expenses']:.2f}")
            print(f"Savings: ${summary['savings']:.2f}")
            print(f"Investments: ${summary['investments']:.2f}")
            print(f"Net: ${summary['net']:.2f}")
            print(f"Savings Rate: {summary['savings_rate']:.1f}%")


if __name__ == "__main__":
    main()