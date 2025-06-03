from flask import Blueprint, render_template
from app.controllers.operation_controller import get_operations
from app.controllers.report_controller import get_total_income, get_total_expense

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def index():
    operations = get_operations(limit=15)
    total_income = get_total_income()
    total_expense = get_total_expense()

    return render_template(
        'dashboard.html',
        operations=operations,
        total_income=total_income,
        total_expense=total_expense
    )
