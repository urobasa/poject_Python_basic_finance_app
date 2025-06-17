from flask_login import login_required, current_user
from flask import Blueprint, render_template, request, redirect, url_for
from app.controllers.account_controller import (
    get_accounts,
    create_account,
    get_account_by_id,
    update_account,
    delete_account
)

accounts_bp = Blueprint('accounts', __name__)


@accounts_bp.route('/')
@login_required
def list_accounts():
    accounts = get_accounts()
    return render_template('accounts/list.html', accounts=accounts)


@accounts_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_account_view():
    if request.method == 'POST':
        name = request.form['name']
        type = request.form['type']
        balance = float(request.form['balance'])
        is_default = bool(request.form.get('is_default'))

        create_account(name, type, balance, is_default)
        return redirect(url_for('accounts.list_accounts'))

    return render_template('accounts/form.html')


@accounts_bp.route('/edit/<int:account_id>', methods=['GET', 'POST'])
@login_required
def edit_account_view(account_id):
    account = get_account_by_id(account_id)
    if not account:
        return redirect(url_for('accounts.list_accounts'))

    if request.method == 'POST':
        name = request.form['name']
        type = request.form['type']
        balance = float(request.form['balance'])
        is_default = bool(request.form.get('is_default'))

        update_account(account_id, name, type, balance, is_default)
        return redirect(url_for('accounts.list_accounts'))

    return render_template('accounts/form.html', account=account)


@accounts_bp.route('/delete/<int:account_id>', methods=['POST'])
@login_required
def delete_account_view(account_id):
    delete_account(account_id)
    return redirect(url_for('accounts.list_accounts'))
