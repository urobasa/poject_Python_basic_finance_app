from app import db

class Account(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(db.String(50), nullable=False)  # наличные, карта, депозит и т.д.
    balance = db.Column(db.Float, nullable=False, default=0.0)
    is_default = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    operations = db.relationship('Operation', backref='account', lazy=True)

    def __repr__(self):
       return f"<Account {self.name} ({self.type}), user_id={self.user_id}>"