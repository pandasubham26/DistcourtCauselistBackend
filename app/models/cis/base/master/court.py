from datetime import datetime

from sqlalchemy import SMALLINT, VARCHAR, TIMESTAMP, INTEGER

from app.extensions import db


class CourtBaseTable(db.Model):
    __tablename__ = 'court_name'
    __abstract__ = True
    __table_args__ = {'schema': 'public', 'extend_existing': True}

    est_code = db.Column(VARCHAR(6), primary_key=True)
    court_name = db.Column(VARCHAR(50), nullable=False)
    state = db.Column(VARCHAR(50), nullable=False)
    district = db.Column(VARCHAR(50), nullable=False)
    create_modify = db.Column(
        TIMESTAMP,
        nullable=False,
        default=datetime.utcnow,
        onupdate=datetime.utcnow
    )