from flask_login import login_required, current_user
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.controllers.category_controller import (
    get_categories, create_category,
    get_category_by_id, update_category,
    delete_category
)

categories_bp = Blueprint('categories', __name__)


@categories_bp.route('/')
@login_required
def list_categories():
    categories = get_categories()
    return render_template('categories/list.html', categories=categories)


@categories_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_category_view():
    if request.method == 'POST':
        name = request.form['name']
        type = request.form['type']
        parent_id = request.form.get('parent_id')
        parent_id = int(parent_id) if parent_id else None

        create_category(name, type, parent_id)
        return redirect(url_for('categories.list_categories'))

    categories = get_categories()
    return render_template('categories/form.html', categories=categories)


@categories_bp.route('/edit/<int:category_id>', methods=['GET', 'POST'])
@login_required
def edit_category_view(category_id):
    category = get_category_by_id(category_id)
    if not category:
        return redirect(url_for('categories.list_categories'))

    if request.method == 'POST':
        name = request.form['name']
        type = request.form['type']
        parent_id = request.form.get('parent_id')
        parent_id = int(parent_id) if parent_id else None

        update_category(category_id, name, type, parent_id)
        return redirect(url_for('categories.list_categories'))

    categories = get_categories()
    return render_template('categories/form.html', category=category, categories=categories)


@categories_bp.route('/delete/<int:category_id>', methods=['POST'])
@login_required
def delete_category_view(category_id):
    new_category_id = request.form.get('new_category_id')

    # Явное преобразование: если указано — привести к int, иначе None
    new_category_id = int(new_category_id) if new_category_id and new_category_id.strip() else None

    success = delete_category(category_id, new_category_id)

    if not success:
        flash('Нельзя удалить категорию с операциями без переноса их в другую категорию.')
    return redirect(url_for('categories.list_categories'))


@categories_bp.route('/confirm_delete/<int:category_id>', methods=['GET', 'POST'])
@login_required
def confirm_delete_category(category_id):
    category = get_category_by_id(category_id)
    if not category:
        flash('Категория не найдена.')
        return redirect(url_for('categories.list_categories'))

    categories = [c for c in get_categories() if c.id != category.id]

    if request.method == 'POST':
        raw = request.form.get('new_category_id')
        try:
            new_category_id = int(raw)
        except (ValueError, TypeError):
            flash('Ошибка: не выбрана новая категория для переноса операций.')
            return redirect(url_for('categories.confirm_delete_category', category_id=category_id))

        print(f"[DEBUG] Удаляем категорию {category_id}, переносим операции в {new_category_id}")

        success = delete_category(category_id, new_category_id)
        if not success:
            flash('Удаление не выполнено.')
        return redirect(url_for('categories.list_categories'))

    return render_template(
        'categories/confirm_delete.html',
        category=category,
        categories=categories
    )
