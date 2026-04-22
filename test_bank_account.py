import pytest
from unittest.mock import MagicMock
from bank_account import BankAccount


# ─────────────────────────────────────────────
# FIXTURES
# ─────────────────────────────────────────────

@pytest.fixture
def mock_db():
    return MagicMock()

@pytest.fixture
def mock_notifier():
    return MagicMock()

@pytest.fixture
def account(mock_db, mock_notifier):
    return BankAccount(
        owner="Alice",
        initial_balance=1000,
        db=mock_db,
        notifier=mock_notifier
    )

@pytest.fixture
def target_account(mock_db, mock_notifier):
    return BankAccount(
        owner="Bob",
        initial_balance=500,
        db=mock_db,
        notifier=mock_notifier
    )


# ─────────────────────────────────────────────
# deposit() tests
# ─────────────────────────────────────────────

def test_deposit_increases_balance(account):
    account.deposit(500)
    assert account.get_balance() == 1500

def test_deposit_calls_db_save(account, mock_db):
    account.deposit(200)
    mock_db.save.assert_called_once()

def test_deposit_calls_notifier(account, mock_notifier):
    account.deposit(200)
    mock_notifier.notify.assert_called_once()

def test_deposit_negative_raises_error(account):
    with pytest.raises(ValueError, match="positive"):
        account.deposit(-100)

def test_deposit_zero_raises_error(account):
    with pytest.raises(ValueError):
        account.deposit(0)


# ─────────────────────────────────────────────
# withdraw() tests
# ─────────────────────────────────────────────

def test_withdraw_decreases_balance(account):
    account.withdraw(300)
    assert account.get_balance() == 700

def test_withdraw_more_than_balance_raises_error(account):
    with pytest.raises(ValueError, match="Insufficient funds"):
        account.withdraw(9999)

def test_withdraw_zero_raises_error(account):
    with pytest.raises(ValueError):
        account.withdraw(0)

def test_withdraw_exact_balance(account):
    account.withdraw(1000)
    assert account.get_balance() == 0


# ─────────────────────────────────────────────
# transfer() tests
# ─────────────────────────────────────────────

def test_transfer_moves_money(account, target_account):
    account.transfer(target_account, 200)
    assert account.get_balance() == 800
    assert target_account.get_balance() == 700

def test_transfer_insufficient_funds_raises_error(account, target_account):
    with pytest.raises(ValueError, match="Insufficient funds"):
        account.transfer(target_account, 9999)

def test_transfer_negative_raises_error(account, target_account):
    with pytest.raises(ValueError):
        account.transfer(target_account, -50)


# ─────────────────────────────────────────────
# frozen account tests
# ─────────────────────────────────────────────

def test_deposit_on_frozen_account_raises_error(account):
    account.freeze_account()
    with pytest.raises(PermissionError, match="frozen"):
        account.deposit(100)

def test_withdraw_on_frozen_account_raises_error(account):
    account.freeze_account()
    with pytest.raises(PermissionError, match="frozen"):
        account.withdraw(100)


# ─────────────────────────────────────────────
# initial balance test
# ─────────────────────────────────────────────

def test_negative_initial_balance_raises_error():
    with pytest.raises(ValueError):
        BankAccount(owner="Test", initial_balance=-500)