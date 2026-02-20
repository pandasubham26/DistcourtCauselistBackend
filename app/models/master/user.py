from werkzeug.security import generate_password_hash, check_password_hash

from app.extensions import db, bcrypt
from sqlalchemy import func


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    estcode = db.Column(db.String(6), nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)
    judge = db.Column(db.String(120), nullable=True)
    role = db.Column(db.String(20), nullable=False)
    isactive = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def group(self) -> str:
        from app.utils import resolve_group_from_role
        return resolve_group_from_role(self.role)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'estcode': self.estcode,
            'judge': self.judge,
            'role': self.role,
            'isactive': self.isactive,
            'created_at': self.created_at.isoformat() if self.created_at else None,
        }
