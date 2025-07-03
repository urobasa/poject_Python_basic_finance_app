from app.models.category import Category
from flask_login import current_user
from app import db
from app.models.operation import Operation
from app.models.account import Account
from datetime import datetime

def create_operation(amount, category_id, account_id, description=None, dt=None):
    dt = dt or datetime.utcnow()

    # Проверка категории
    category = Category.query.filter_by(id=category_id, user_id=current_user.id).first()
    if not category:
        return None  # сигнал в контроллер вью о проблеме

    dt = dt or datetime.utcnow()
    operation = Operation(
        amount=amount,
        category_id=category_id,
        account_id=account_id,
        description=description,
        datetime=dt,
        user_id=current_user.id)
    db.session.add(operation)

    # Обновим баланс счёта
    account = Account.query.get(account_id)
    category_type = category.type
    if category_type == 'expense':
        account.balance -= amount
    else:
        account.balance += amount
    db.session.commit()
    return operation

def get_operations(limit=50):
    return Operation.query.filter_by(user_id=current_user.id).order_by(Operation.datetime.desc()).limit(limit).all()

def delete_operation(operation_id):
    operation = Operation.query.filter_by(id=operation_id, user_id=current_user.id).first()
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


def get_operations_filtered(category_id=None, start_date=None, end_date=None, amount_min=None, amount_max=None, op_type=None):
    query = Operation.query.filter_by(user_id=current_user.id)

    if category_id:
        query = query.filter_by(category_id=category_id)
    if start_date:
        query = query.filter(Operation.datetime >= start_date)
    if end_date:
        query = query.filter(Operation.datetime <= end_date)
    if amount_min is not None:
        query = query.filter(Operation.amount >= amount_min)
    if amount_max is not None:
        query = query.filter(Operation.amount <= amount_max)
    if op_type in ['income', 'expense']:
        query = query.join(Operation.category).filter_by(type=op_type)

    return query.order_by(Operation.datetime.desc(), Operation.id.desc()).all()
