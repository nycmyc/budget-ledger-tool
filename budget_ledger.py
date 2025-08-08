#!/usr/bin/env python3
"""
Budget Ledger Tool
A simple calculator/ledger for personal finance tracking
"""

import datetime
import json
from typing import Dict, List
from pathlib import Path
from collections import defaultdict


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
        # Account types for tracking where money is
        self.account_types = ['bank', 'cash', 'invested', 'crypto', 'other']
        self.load_data()
    
    def add_transaction(self, amount: float, category: str, subcategory: str, 
                       description: str = "", account: str = "bank"):
        """Add a new transaction to the ledger"""
        transaction = {
            'date': datetime.datetime.now().isoformat(),
            'amount': amount,
            'category': category,
            'subcategory': subcategory,
            'description': description,
            'account': account  # New field for account type
        }
        self.transactions.append(transaction)
        self.save_data()
        return transaction
    
    def get_balance(self) -> float:
        """Calculate current balance (income - expenses)"""
        income = sum(t['amount'] for t in self.transactions if t['category'] == 'income')
        expenses = sum(t['amount'] for t in self.transactions if t['category'] == 'expenses')
        return income - expenses
    
    def get_account_breakdown(self) -> Dict[str, float]:
        """Get balance broken down by account type"""
        breakdown = defaultdict(float)
        
        for transaction in self.transactions:
            # For backward compatibility, check if 'account' exists
            # If not, try to infer from description
            if 'account' in transaction:
                account = transaction['account']
            else:
                # Try to infer from description (for old data)
                desc_lower = transaction.get('description', '').lower()
                if 'cash' in desc_lower:
                    account = 'cash'
                elif 'bank' in desc_lower:
                    account = 'bank'
                elif 'invest' in desc_lower:
                    account = 'invested'
                else:
                    account = 'bank'  # default
            
            # Add or subtract based on category
            if transaction['category'] == 'income':
                breakdown[account] += transaction['amount']
            elif transaction['category'] == 'expenses':
                breakdown[account] -= transaction['amount']
            elif transaction['category'] == 'investments':
                # Money moved from bank/cash to invested
                breakdown['invested'] += transaction['amount']
                # You might want to track which account it came from
                breakdown['bank'] -= transaction['amount']
        
        # Calculate net total
        breakdown['net'] = sum(v for k, v in breakdown.items() if k != 'net')
        
        return dict(breakdown)
    
    def display_balance_table(self):
        """Display formatted balance table"""
        breakdown = self.get_account_breakdown()
        
        # Print header with date
        print(f"\n{datetime.datetime.now().strftime('%m/%d/%y')}")
        print("=" * 40)
        
        # Print each account type
        accounts_to_show = ['bank', 'cash', 'invested']
        for account in accounts_to_show:
            value = breakdown.get(account, 0)
            print(f"{account.capitalize():<20} {value:>15.2f}")
        
        print("-" * 40)
        print(f"{'Net':<20} {breakdown.get('net', 0):>15.2f}")
        print("=" * 40)
    
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
    
    def migrate_data(self):
        """Add account field to old transactions based on description"""
        updated = False
        for transaction in self.transactions:
            if 'account' not in transaction:
                desc_lower = transaction.get('description', '').lower()
                if 'cash' in desc_lower:
                    transaction['account'] = 'cash'
                elif 'bank' in desc_lower:
                    transaction['account'] = 'bank'
                elif 'invest' in desc_lower:
                    transaction['account'] = 'invested'
                else:
                    transaction['account'] = 'bank'
                updated = True
        
        if updated:
            self.save_data()
            print("✓ Migrated old transactions to include account field")


def main():
    """Main CLI interface"""
    ledger = BudgetLedger()
    
    # Migrate old data if needed
    ledger.migrate_data()
    
    while True:
        print("\n=== Budget Ledger Tool ===")
        
        # Show account breakdown
        ledger.display_balance_table()
        
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
            
            # Ask for account type
            print(f"Account type: {', '.join(ledger.account_types)}")
            account = input("Account (default: bank): ").lower() or 'bank'
            
            print(f"Subcategories: {', '.join(ledger.categories[category])}")
            subcategory = input("Subcategory: ")
            description = input("Description (optional): ")
            
            ledger.add_transaction(amount, category, subcategory, description, account)
            print(f"✓ Transaction added to {account}!")
        
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