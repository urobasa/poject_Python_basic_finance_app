from flask_login import login_required, current_user
from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.controllers.category_controller import (
    create_category,
    get_category_by_id, update_category,
    delete_category
)
from app.models.category import Category
categories_bp = Blueprint('categories', __name__)
@categories_bp.route('/')
@login_required
def list_categories():
    tree = Category.get_tree(user_id=current_user.id)
    categories = Category.flatten_tree(tree)
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

    categories = Category.flatten_tree(Category.get_tree(user_id=current_user.id))
    return render_template('categories/form.html', categories=categories)

@categories_bp.route('/edit/<int:category_id>', methods=['GET', 'POST'])
@login_required
def edit_category_view(category_id):
    def get_category_path(category):
        parts = []
        current = Category.query.get(category.parent_id) if category.parent_id else None
        while current:
            parts.append(current.name)
            current = Category.query.get(current.parent_id) if current.parent_id else None
        if parts:
            return " -> ".join(reversed(parts))
        else:
            return "Корневая категория"

    category = get_category_by_id(category_id)
    if not category:
        flash('Категория не найдена.', 'danger')
        return redirect(url_for('categories.list_categories'))

    if request.method == 'POST':
        name = request.form['name']
        type = request.form['type']
        parent_id = request.form.get('parent_id')
        parent_id = int(parent_id) if parent_id else None

        # Если выбран родитель — проверяем его существование и совпадение типа
        if parent_id is not None:
            parent_category = get_category_by_id(parent_id)
            if not parent_category:
                flash('Выбранная родительская категория не существует.', 'danger')
                categories = Category.flatten_tree(Category.get_tree(user_id=current_user.id))
                category_path = get_category_path(category)
                return render_template('categories/form.html', category=category, categories=categories, category_path=category_path)

            if parent_category.type != type:
                flash('Тип категории и родительской категории должны совпадать.', 'danger')
                categories = Category.flatten_tree(Category.get_tree(user_id=current_user.id))
                category_path = get_category_path(category)
                return render_template('categories/form.html', category=category, categories=categories, category_path=category_path)

        update_category(category_id, name, type, parent_id)
        flash('Категория успешно обновлена.', 'success')
        return redirect(url_for('categories.list_categories'))

    categories = Category.flatten_tree(Category.get_tree(user_id=current_user.id))
    category_path = get_category_path(category)
    return render_template('categories/form.html', category=category, categories=categories, category_path=category_path)


@categories_bp.route('/delete/<int:category_id>', methods=['POST'])
@login_required
def delete_category_view(category_id):
    success = delete_category(category_id)

    if not success:
        flash('Нельзя удалить категорию с операциями.')
    return redirect(url_for('categories.list_categories'))


@categories_bp.route('/confirm_delete/<int:category_id>', methods=['GET', 'POST'])
@login_required
def confirm_delete_category(category_id):
    category = Category.query.filter_by(id=category_id, user_id=current_user.id).first()
    categories = Category.flatten_tree(Category.get_tree(user_id=current_user.id))

    if not category:
        flash('Категория не найдена.')
        return redirect(url_for('categories.list_categories'))

    if request.method == 'POST':
        success = delete_category(category_id)
        if not success:
            flash('Удаление не выполнено.')
        return redirect(url_for('categories.list_categories'))

    return render_template(
        'categories/confirm_delete.html',
        category=category,
        categories=categories
    )
