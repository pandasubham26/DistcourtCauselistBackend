from datetime import datetime

from sqlalchemy import SMALLINT, VARCHAR, TIMESTAMP, INTEGER

from app.extensions import db


class DistrictBaseTable(db.Model):
    __tablename__ = 'district_t'
    __abstract__ = True
    __table_args__ = {'schema': 'public', 'extend_existing': True}

    dist_code = db.Column(SMALLINT, primary_key=True)
    state_id = db.Column(INTEGER)
    dist_name = db.Column(VARCHAR(50))
    display = db.Column(VARCHAR(1), nullable=False, default='Y')
    create_modify = db.Column(TIMESTAMP, default=datetime.utcnow)