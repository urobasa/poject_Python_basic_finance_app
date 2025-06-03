from app import db

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(10), nullable=False)  # 'income' или 'expense'
    parent_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)

    parent = db.relationship('Category', remote_side=[id], backref='children')
    operations = db.relationship('Operation', backref='category', lazy=True)

    def __repr__(self):
        return f'<Category {self.name}>'
