from app import db

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(10), nullable=False)  # 'income' или 'expense'
    parent_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    parent = db.relationship('Category', remote_side=[id], backref='children')
    operations = db.relationship('Operation', backref='category', lazy=True)

    def __repr__(self):
        return f"<Category {self.name} ({self.type}), user_id={self.user_id}>"

    @classmethod
    def get_tree(cls, user_id, type=None):
        query = cls.query.filter_by(user_id=user_id)
        if type:
            query = query.filter_by(type=type)
        categories = query.all()

        category_dict = {c.id: c for c in categories}
        for cat in categories:
            cat.children_nodes = []
        for cat in categories:
            if cat.parent_id and cat.parent_id in category_dict:
                category_dict[cat.parent_id].children_nodes.append(cat)

        return [c for c in categories if c.parent_id is None]

    @staticmethod
    def flatten_tree(tree, level=0):
        result = []
        for node in tree:
            result.append({
                'id': node.id,
                'name': node.name,
                'type': node.type,
                'parent_id': node.parent_id,
                'level': level,
                'has_children': bool(getattr(node, 'children_nodes', []))
            })
            if hasattr(node, 'children_nodes'):
                result.extend(Category.flatten_tree(node.children_nodes, level + 1))
        return result

    @classmethod
    def get_root_map(cls, user_id):
        categories = cls.query.filter_by(user_id=user_id).all()
        category_by_id = {c.id: c for c in categories}
        root_map = {}

        def find_root(cat):
            while cat.parent_id:
                cat = category_by_id.get(cat.parent_id)
            return cat

        for cat in categories:
            root = find_root(cat)
            root_map[cat.id] = root.name

        return root_map

    def get_amount_in_period(self, user_id, start_date, end_date):
        from app.models.operation import Operation
        from app.extensions import db
        query = db.session.query(db.func.sum(Operation.amount))             .filter(Operation.user_id == user_id)             .filter(Operation.category_id == self.id)
        if start_date:
            query = query.filter(Operation.datetime >= start_date)
        if end_date:
            query = query.filter(Operation.datetime <= end_date)
        total = query.scalar() or 0
        # Рекурсивно добавить суммы вложенных категорий
        for child in self.children:
            total += child.get_amount_in_period(user_id, start_date, end_date)
        return total
