from app import db
from app.models.operation import Operation
from app.models.account import Account
from datetime import datetime

def create_operation(amount, category_id, account_id, description=None, dt=None):
    dt = dt or datetime.utcnow()

    operation = Operation(
        amount=amount,
        category_id=category_id,
        account_id=account_id,
        description=description,
        datetime=dt
    )

    db.session.add(operation)

    # Обновим баланс счёта
    account = Account.query.get(account_id)
    category_type = operation.category.type
    if category_type == 'expense':
        account.balance -= amount
    else:
        account.balance += amount

    db.session.commit()
    return operation

def get_operations(limit=15):
    return Operation.query.order_by(Operation.datetime.desc()).limit(limit).all()

def get_operations_filtered(category_id=None, start_date=None, end_date=None):
    query = Operation.query

    if category_id:
        query = query.filter_by(category_id=category_id)
    if start_date:
        query = query.filter(Operation.datetime >= start_date)
    if end_date:
        query = query.filter(Operation.datetime <= end_date)

    return query.order_by(Operation.datetime.desc()).all()

def delete_operation(operation_id):
    operation = Operation.query.get(operation_id)
    if not operation:
        return False

    account = Account.query.get(operation.account_id)
    if operation.category.type == 'expense':
        account.balance += operation.amount
    else:
        account.balance -= operation.amount

    db.session.delete(operation)
    db.session.commit()
    return True
