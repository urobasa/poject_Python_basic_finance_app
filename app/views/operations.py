from flask import Blueprint, render_template, request, redirect, url_for
from datetime import datetime

from app.controllers.operation_controller import create_operation, get_operations_filtered
from app.controllers.category_controller import get_categories
from app.controllers.account_controller import get_accounts

operations_bp = Blueprint('operations', __name__)

@operations_bp.route('/')
def list_operations():
    category_id = request.args.get('category_id', type=int)
    start_date = request.args.get('start_date')
    end_date = request.args.get('end_date')

    operations = get_operations_filtered(category_id, start_date, end_date)
    return render_template('operations/list.html', operations=operations)


@operations_bp.route('/create', methods=['GET', 'POST'])
def create_operation_view():
    if request.method == 'POST':
        amount = float(request.form['amount'])
        category_id = int(request.form['category_id'])
        account_id = int(request.form['account_id'])
        description = request.form.get('description')

        # Получаем значения из двух отдельных полей
        date_str = request.form.get('date')      # ожидается 'YYYY-MM-DD'
        time_str = request.form.get('time')      # ожидается 'HH:MM'

        # Преобразуем в datetime, если оба поля указаны
        if date_str and time_str:
            dt = datetime.strptime(f'{date_str} {time_str}', '%Y-%m-%d %H:%M')
        else:
            dt = datetime.now()  # fallback на текущий момент

        create_operation(amount, category_id, account_id, description, dt)
        return redirect(url_for('operations.list_operations'))

    categories = get_categories()
    accounts = get_accounts()
    return render_template(
        'operations/form.html',
        categories=categories,
        accounts=accounts,
        now=datetime.now()
    )

