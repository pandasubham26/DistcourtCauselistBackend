from datetime import datetime

from sqlalchemy import SMALLINT, VARCHAR, TIMESTAMP, INTEGER

from app.extensions import db


class DesignationBaseTable(db.Model):
    __tablename__ = 'desg_t'
    __abstract__ = True
    __table_args__ = {'schema': 'public', 'extend_existing': True}

    desgcode = db.Column(INTEGER, primary_key=True)
    desgname = db.Column(VARCHAR(100), nullable=False)
    display = db.Column(VARCHAR(1), nullable=False, default='Y')
    create_modify = db.Column(TIMESTAMP, default=datetime.utcnow)