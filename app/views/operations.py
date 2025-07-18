from flask_login import login_required, current_user
from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime

from app.controllers.operation_controller import create_operation, get_operations_filtered
from app.controllers.account_controller import get_accounts, get_default_account
from app.models.category import Category
from app.models.account import Account

operations_bp = Blueprint('operations', __name__)

@operations_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_operation_view():
    categories = Category.flatten_tree(Category.get_tree(user_id=current_user.id))
    accounts = [acc for acc in get_accounts() if acc.user_id == current_user.id]
    default_account = get_default_account()
    default_account_id = default_account.id if default_account else None

    if request.method == 'POST':
        amount = float(request.form['amount'])
        category_id_raw = request.form.get('category_id')

        if not category_id_raw:
            flash('Категория не выбрана.', 'danger')
            return render_template(
                'operations/form.html',
                categories=categories,
                accounts=accounts,
                default_account_id=default_account_id,
                now=datetime.now(),
                form_data=request.form
            )

        category_id = int(category_id_raw)
        account_id = int(request.form['account_id'])
        description = request.form.get('description')

        account = Account.query.filter_by(id=account_id, user_id=current_user.id).first()
        if not account:
            flash("Счет не найден.", "danger")
            return render_template(
                'operations/form.html',
                categories=categories,
                accounts=accounts,
                default_account_id=default_account_id,
                now=datetime.now(),
                form_data=request.form
            )

        category = Category.query.filter_by(id=category_id, user_id=current_user.id).first()
        if not category:
            flash("Категория не найдена.", "danger")
            return render_template(
                'operations/form.html',
                categories=categories,
                accounts=accounts,
                default_account_id=default_account_id,
                now=datetime.now(),
                form_data=request.form
            )

        operation_type = category.type

        if operation_type == 'expense' and account.balance - amount < 0:
            flash(f"На счете {account.name} недостаточно средств для операции.", "danger")
            return render_template(
                'operations/form.html',
                categories=categories,
                accounts=accounts,
                default_account_id=default_account_id,
                now=datetime.now(),
                form_data=request.form
            )

        date_str = request.form.get('date')
        time_str = request.form.get('time')

        if date_str and time_str:
            dt = datetime.strptime(f'{date_str} {time_str}', '%Y-%m-%d %H:%M')
        else:
            dt = datetime.now()

        create_operation(amount, category_id, account_id, description, dt)
        return redirect(url_for('operations.list_operations'))

    return render_template(
        'operations/form.html',
        categories=categories,
        accounts=accounts,
        default_account_id=default_account_id,
        now=datetime.now(),
        form_data=None
    )

@operations_bp.route('/')
@operations_bp.route('/operations/')
@login_required
def list_operations():
    start_date = request.args.get("start_date")
    end_date = request.args.get("end_date")
    amount_min = request.args.get("amount_min", type=float)
    amount_max = request.args.get("amount_max", type=float)
    category_id = request.args.get("category_id", type=int)
    op_type = request.args.get("type")

    operations = get_operations_filtered(
        start_date=start_date,
        end_date=end_date,
        amount_min=amount_min,
        amount_max=amount_max,
        category_id=category_id,
        op_type=op_type,
    )

    categories = Category.query.filter_by(user_id=current_user.id).all()

    return render_template("operations/list.html", operations=operations, categories=categories, request=request)
