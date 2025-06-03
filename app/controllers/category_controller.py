from app import db
from app.models.category import Category
from app.models.operation import Operation

def create_category(name, type, parent_id=None):
    category = Category(name=name, type=type, parent_id=parent_id)
    db.session.add(category)
    db.session.commit()
    return category

def get_categories(type=None):
    if type:
        return Category.query.filter_by(type=type).all()
    return Category.query.all()

def get_category_by_id(category_id):
    return Category.query.get(category_id)

def update_category(category_id, name, type, parent_id=None):
    category = Category.query.get(category_id)
    if category:
        category.name = name
        category.type = type
        category.parent_id = parent_id
        db.session.commit()
    return category

def delete_category(category_id, new_category_id=None):
    category = Category.query.get(category_id)
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
