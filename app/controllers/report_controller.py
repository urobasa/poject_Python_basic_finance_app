from flask_login import current_user
from app.models.operation import Operation
from app.models.category import Category
from sqlalchemy import func
from datetime import datetime

from app import db

def get_summary(start_date=None, end_date=None):
    query = db.session.query(
        Category.name,
        Category.type,
        func.sum(Operation.amount)
    ).join(Operation.category).filter(Operation.user_id == current_user.id)

    if start_date:
        query = query.filter(Operation.datetime >= start_date)
    if end_date:
        query = query.filter(Operation.datetime <= end_date)

    query = query.group_by(Category.name, Category.type)
    return query.all()

def get_totals_by_type(start_date=None, end_date=None):
    query = db.session.query(
        Category.type,
        func.sum(Operation.amount)
    ).join(Operation.category).filter(Operation.user_id == current_user.id)

    if start_date:
        query = query.filter(Operation.datetime >= start_date)
    if end_date:
        query = query.filter(Operation.datetime <= end_date)

    query = query.group_by(Category.type)
    return dict(query.all())

def get_total_income(start_date=None, end_date=None):
    totals = get_totals_by_type(start_date, end_date)
    return totals.get('income', 0)

def get_total_expense(start_date=None, end_date=None):
    totals = get_totals_by_type(start_date, end_date)
    return totals.get('expense', 0)
