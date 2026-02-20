from datetime import datetime

from sqlalchemy import SMALLINT, VARCHAR, TIMESTAMP

from app.extensions import db


class StateBaseTable(db.Model):
    __tablename__ = 'state'
    __abstract__ = True
    __table_args__ = {'schema': 'public', 'extend_existing': True}

    state_id = db.Column(SMALLINT, primary_key=True)
    state = db.Column(VARCHAR(50))
    est_code_src = db.Column(VARCHAR(6))
    display = db.Column(VARCHAR(1), nullable=False, default='Y')
    create_modify = db.Column(TIMESTAMP, default=datetime.utcnow)