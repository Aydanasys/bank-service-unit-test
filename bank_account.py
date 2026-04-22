from database import Database
from notifier import Notifier


class BankAccount:
    def __init__(self, owner: str, initial_balance: float = 0,
                 db: Database = None, notifier: Notifier = None):
        if initial_balance < 0:
            raise ValueError("Initial balance cannot be negative")
        self.owner = owner
        self.balance = initial_balance
        self.is_frozen = False
        self._history = []
        self.db = db
        self.notifier = notifier

    def deposit(self, amount: float) -> float:
        if self.is_frozen:
            raise PermissionError("Account is frozen")
        if amount <= 0:
            raise ValueError("Amount must be positive")
        self.balance += amount
        self._history.append({"type": "deposit", "amount": amount})
        if self.db:
            self.db.save({"owner": self.owner, "balance": self.balance})
        if self.notifier:
            self.notifier.notify(f"Deposit: +{amount}")
        return self.balance

    def withdraw(self, amount: float) -> float:
        if self.is_frozen:
            raise PermissionError("Account is frozen")
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient funds")
        self.balance -= amount
        self._history.append({"type": "withdraw", "amount": amount})
        if self.db:
            self.db.save({"owner": self.owner, "balance": self.balance})
        if self.notifier:
            self.notifier.notify(f"Withdrawal: -{amount}")
        return self.balance

    def transfer(self, target: "BankAccount", amount: float) -> bool:
        if self.is_frozen:
            raise PermissionError("Account is frozen")
        if amount <= 0:
            raise ValueError("Amount must be positive")
        if amount > self.balance:
            raise ValueError("Insufficient funds for transfer")
        self.withdraw(amount)
        target.deposit(amount)
        return True

    def get_balance(self) -> float:
        return self.balance

    def freeze_account(self):
        """Intentionally not tested — added to test debt"""
        self.is_frozen = True

    def transaction_history(self):
        """Intentionally not tested — added to test debt"""
        if self.db:
            return self.db.get_history(self.owner)
        return self._history