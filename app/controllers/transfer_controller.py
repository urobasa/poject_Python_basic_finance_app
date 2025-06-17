from flask_login import current_user
from app import db
from app.models.transfer import Transfer
from app.models.account import Account

def create_transfer(from_account_id, to_account_id, amount, description=None, dt=None):
    if from_account_id == to_account_id:
        raise ValueError("Счета должны быть разными")

    from_account = Account.query.filter_by(id=from_account_id, user_id=current_user.id).first()
    to_account = Account.query.filter_by(id=to_account_id, user_id=current_user.id).first()

    if not from_account or not to_account:
        raise ValueError("Один из счетов не найден или не принадлежит текущему пользователю")

    if from_account.balance < amount:
        raise ValueError("Недостаточно средств для перевода")

    transfer = Transfer(
        from_account_id=from_account_id,
        to_account_id=to_account_id,
        amount=amount,
        description=description,
        datetime=dt
    , user_id=current_user.id)

    from_account.balance -= amount
    to_account.balance += amount

    db.session.add(transfer)
    db.session.commit()
    return transfer

def get_transfers():
    return Transfer.query.filter_by(user_id=current_user.id).order_by(Transfer.datetime.desc()).all()
