from flask import Blueprint, render_template, redirect, url_for, request, flash, abort
from flask_login import login_required, current_user
from functools import wraps
from app.models.user import User
from app import db

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(func):
    @wraps(func)
    def decorated_view(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            abort(403)
        return func(*args, **kwargs)
    return decorated_view

@admin_bp.route('/users')
@login_required
@admin_required
def user_list():
    users = User.query.all()
    return render_template('admin/user_list.html', users=users, active_tab='users')


@admin_bp.route('/users/add', methods=['GET', 'POST'])
@login_required
@admin_required
def user_add():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Пользователь с таким именем уже существует.')
            return redirect(url_for('admin.user_add'))
        user = User(username=username)
        user.set_password(password)
        user.is_admin = 'is_admin' in request.form
        db.session.add(user)
        db.session.commit()
        flash('Пользователь добавлен.')
        return redirect(url_for('admin.user_list'))
    return render_template('admin/user_add.html')

@admin_bp.route('/users/<int:user_id>/edit', methods=['GET', 'POST'])
@login_required
@admin_required
def user_edit(user_id):
    user = User.query.get_or_404(user_id)
    if request.method == 'POST':
        password = request.form.get('password')
        user.is_admin = 'is_admin' in request.form
        if password:
            user.set_password(password)
        db.session.commit()
        flash('Пользователь обновлён.')
        return redirect(url_for('admin.user_list'))
    return render_template('admin/user_edit.html', user=user)

@admin_bp.route('/users/<int:user_id>/delete')
@login_required
@admin_required
def user_delete(user_id):
    user = User.query.get_or_404(user_id)
    if user.id == current_user.id:
        flash('Нельзя удалить самого себя.')
        return redirect(url_for('admin.user_list'))
    db.session.delete(user)
    db.session.commit()
    flash('Пользователь удалён.')
    return redirect(url_for('admin.user_list'))




@admin_bp.route('/test-data', methods=['GET', 'POST'])
@login_required
@admin_required
def test_data():
    from app.models.user import User
    from app.models.account import Account
    from app.models.category import Category
    from app import db
    from faker import Faker
    import random

    fake = Faker('ru_RU')

    EXPENSE_CATEGORY_TREE = {
        "Продукты": ["Молочные", "Мясные", "Овощи", "Фрукты", "Снеки"],
        "Транспорт": ["Метро", "Такси", "Автомобиль", "Авиабилеты"],
        "Жильё": ["Аренда", "Коммунальные услуги", "Ремонт"],
        "Здоровье": ["Аптека", "Клиника", "Страховка"],
        "Развлечения": ["Кино", "Театр", "Подписки", "Подарки"]
    }

    INCOME_CATEGORY_TREE = {
        "Доходы": ["Зарплата", "Фриланс", "Инвестиции", "Подарки", "Гранты"]
    }

    if request.method == 'POST':
        for _ in range(3):
            username = fake.user_name()
            if not User.query.filter_by(username=username).first():
                u = User(username=username, is_admin=False)
                u.set_password('123')
                db.session.add(u)
                db.session.flush()

                # Счета
                for _ in range(2):
                    card_name = f"{fake.credit_card_provider()} {random.randint(100, 999)}"
                    acc = Account(
                        name=card_name,
                        type=random.choice(["наличные", "карта", "депозит"]),
                        balance=random.randint(1000, 10000),
                        user_id=u.id
                    )
                    db.session.add(acc)

                # Категории расхода (3 уровня: вручную + Faker)
                for root, children in EXPENSE_CATEGORY_TREE.items():
                    parent = Category(name=root, type='expense', user_id=u.id)
                    db.session.add(parent)
                    db.session.flush()

                    for sub in children:
                        child = Category(name=sub, type='expense', user_id=u.id, parent_id=parent.id)
                        db.session.add(child)
                        db.session.flush()

                        for _ in range(2):
                            grandchild = Category(
                                name=fake.word().capitalize(),
                                type='expense',
                                user_id=u.id,
                                parent_id=child.id
                            )
                            db.session.add(grandchild)

                # Категории дохода (3 уровня: вручную + Faker)
                for root, children in INCOME_CATEGORY_TREE.items():
                    parent = Category(name=root, type='income', user_id=u.id)
                    db.session.add(parent)
                    db.session.flush()

                    for sub in children:
                        child = Category(name=sub, type='income', user_id=u.id, parent_id=parent.id)
                        db.session.add(child)
                        db.session.flush()

                        for _ in range(2):
                            grandchild = Category(
                                name=fake.job().split()[0],
                                type='income',
                                user_id=u.id,
                                parent_id=child.id
                            )
                            db.session.add(grandchild)

        db.session.commit()
        flash('Тестовые данные успешно созданы. Пароль всех тестовых пользователей: 123', 'success')
        return redirect(url_for('admin.test_data'))

    return render_template('admin/test_data.html', active_tab='test')

@admin_bp.route('/generate-operations', methods=['POST'])
@login_required
@admin_required

def generate_operations():
    from app.models import User, Account, Category, Operation
    from app import db
    from faker import Faker
    import random
    from datetime import datetime, timedelta

    fake = Faker('ru_RU')

    users = User.query.all()

    income_comments = [
        lambda: f"Перевод от {fake.first_name()}",
        lambda: f"Оплата от {fake.company()}",
        lambda: f"Доход от {fake.job().split()[0]}",
        lambda: "Бонус за работу",
        lambda: "Получено на счёт"
    ]

    expense_comments = [
        lambda: f"Оплата {fake.company()}",
        lambda: f"Покупка в {fake.city()}",
        lambda: f"Трата на {fake.word()}",
        lambda: "Покупка по акции",
        lambda: "Расход в магазине"
    ]

    for user in users:
        accounts = Account.query.filter_by(user_id=user.id).all()
        if not accounts:
            continue

        income_categories = Category.query.filter_by(user_id=user.id, type='income').all()
        expense_categories = Category.query.filter_by(user_id=user.id, type='expense').all()

        def get_valid_accounts():
            return [a for a in accounts if a.balance > 0]

        # 15 доходов
        for _ in range(15):
            if not income_categories:
                break
            amount = random.randint(50, 150)
            account = random.choice(accounts)
            category = random.choice(income_categories)

            op = Operation(
                user_id=user.id,
                amount=amount,
                account_id=account.id,
                category_id=category.id,
                datetime=fake.date_time_between(start_date='-2M', end_date='now'),
                description=random.choice(income_comments)()
            )
            db.session.add(op)
            account.balance += amount

        # Расходы до обнуления
        while True:
            valid_accounts = get_valid_accounts()
            if not valid_accounts or not expense_categories:
                break

            account = random.choice(valid_accounts)
            max_amount = account.balance
            amount = random.randint(1, min(100, int(max_amount)))
            category = random.choice(expense_categories)

            op = Operation(
                user_id=user.id,
                amount=amount,
                account_id=account.id,
                category_id=category.id,
                datetime=fake.date_time_between(start_date='-2M', end_date='now'),
                description=random.choice(expense_comments)()
            )
            db.session.add(op)
            account.balance -= amount

    db.session.commit()
    flash('Операции успешно сгенерированы.', 'success')
    return redirect(url_for('admin.test_data'))

