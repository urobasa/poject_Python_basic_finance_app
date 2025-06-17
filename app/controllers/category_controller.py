from flask_login import current_user
from app import db
from app.models.category import Category
from app.models.operation import Operation

def create_category(name, type, parent_id=None):
    category = Category(name=name, type=type, parent_id=parent_id, user_id=current_user.id)
    db.session.add(category)
    db.session.commit()
    return category

def get_categories(type=None):
    if type:
        return Category.query.filter_by(user_id=current_user.id, type=type).all()
    return Category.query.filter_by(user_id=current_user.id).all()

def get_category_by_id(category_id):
    category = Category.query.filter_by(id=category_id, user_id=current_user.id).first()
    return category

def update_category(category_id, name, type, parent_id=None):
    category = Category.query.filter_by(id=category_id, user_id=current_user.id).first()
    if category:
        category.name = name
        category.type = type
        category.parent_id = parent_id
        db.session.commit()
    return category

def delete_category(category_id, new_category_id=None):
    category = Category.query.filter_by(id=category_id, user_id=current_user.id).first()
    if not category:
        return False

    if category.operations:
        if new_category_id is None:
            return False

        for op in category.operations:
            op.category_id = new_category_id
            db.session.add(op)

    db.session.delete(category)
    db.session.commit()
    return True
