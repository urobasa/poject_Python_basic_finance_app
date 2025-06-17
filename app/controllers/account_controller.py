from flask_login import current_user
from app import db
from app.models.account import Account

def create_account(name, type, balance=0.0, is_default=False):
    if is_default:
       Account.query.filter_by(user_id=current_user.id).update({Account.is_default: False})
    user_id = current_user.id
    account = Account(name=name, type=type, balance=balance, is_default=is_default, user_id=user_id)
    db.session.add(account)
    db.session.commit()
    return account

def get_accounts():
    return Account.query.filter_by(user_id=current_user.id).all()

def get_account_by_id(account_id):
    return Account.query.filter_by(id=account_id, user_id=current_user.id).first()

def update_account(account_id, name, type, balance, is_default):
    account = Account.query.filter_by(id=account_id, user_id=current_user.id).first()
    if account:
        if is_default:
            Account.query.filter_by(user_id=current_user.id).update({Account.is_default: False})
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

def get_default_account():
    return Account.query.filter_by(user_id=current_user.id, is_default=True).first()

