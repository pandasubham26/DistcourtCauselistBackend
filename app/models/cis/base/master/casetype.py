from datetime import datetime

from sqlalchemy import SMALLINT, VARCHAR, TIMESTAMP, INTEGER

from app.extensions import db


class CaseTypeBaseTable(db.Model):
    __tablename__ = 'case_type_t'
    __abstract__ = True
    __table_args__ = {'schema': 'public', 'extend_existing': True}

    case_type = db.Column(SMALLINT, primary_key=True, default=0)
    type_name = db.Column(VARCHAR(50))
    full_form = db.Column(VARCHAR(100))
    type_flag = db.Column(INTEGER, nullable=False, default='1')
    display = db.Column(VARCHAR(1), nullable=False, default='Y')
    create_modify = db.Column(TIMESTAMP, default=datetime.utcnow)