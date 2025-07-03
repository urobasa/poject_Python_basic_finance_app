
from app.models.category import Category
from app.models.operation import Operation
from sqlalchemy import func
from app.extensions import db

def get_summary_table(user_id, start_date, end_date):
    tree = Category.get_tree(user_id=user_id)
    categories = []

    def traverse_and_sum(cat, level=0):
        cat.amount = cat.get_amount_in_period(user_id, start_date, end_date)
        cat.level = level
        cat.has_children = bool(cat.children)  # Добавим признак наличия детей
        categories.append(cat)
        for child in cat.children:
            traverse_and_sum(child, level + 1)

    for root_cat in tree:
        traverse_and_sum(root_cat)

    return categories

def get_summary_by_period(start_date, end_date):
    summary = db.session.query(Category.name, func.sum(Operation.amount).label('amount'))         .join(Operation, Operation.category_id == Category.id)         .filter(Operation.datetime >= start_date)         .filter(Operation.datetime <= end_date)         .group_by(Category.name)         .all()
    return summary

def get_total_income(user_id, start_date=None, end_date=None):
    query = db.session.query(func.sum(Operation.amount))         .join(Category, Category.id == Operation.category_id)         .filter(Category.type == 'income', Operation.user_id == user_id)
    if start_date:
        query = query.filter(Operation.datetime >= start_date)
    if end_date:
        query = query.filter(Operation.datetime <= end_date)
    total_income = query.scalar() or 0
    return total_income

def get_total_expense(user_id, start_date=None, end_date=None):
    query = db.session.query(func.sum(Operation.amount))         .join(Category, Category.id == Operation.category_id)         .filter(Category.type == 'expense', Operation.user_id == user_id)
    if start_date:
        query = query.filter(Operation.datetime >= start_date)
    if end_date:
        query = query.filter(Operation.datetime <= end_date)
    total_expense = query.scalar() or 0
    return total_expense
