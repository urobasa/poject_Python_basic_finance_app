from app import db
from app.models.account import Account

def create_account(name, type, balance=0.0, is_default=False):
    if is_default:
        # Снимаем флаг default со всех других счетов
        Account.query.update({Account.is_default: False})
    account = Account(name=name, type=type, balance=balance, is_default=is_default)
    db.session.add(account)
    db.session.commit()
    return account

def get_accounts():
    return Account.query.all()

def get_account_by_id(account_id):
    return Account.query.get(account_id)

def update_account(account_id, name, type, balance, is_default):
    account = Account.query.get(account_id)
    if account:
        if is_default:
            Account.query.update({Account.is_default: False})
        account.name = name
        account.type = type
        account.balance = balance
        account.is_default = is_default
        db.session.commit()
    return account

def delete_account(account_id):
    account = Account.query.get(account_id)
    if account:
        db.session.delete(account)
        db.session.commit()
