from datetime import datetime

from sqlalchemy.dialects.postgresql import TIMESTAMP, VARCHAR, INTEGER
from sqlalchemy import text

from app.extensions import db


class Taluka(db.Model):
    __tablename__ = 'taluka_t'
    __table_args__ = {'schema': 'public'}

    taluka_code = db.Column(INTEGER, primary_key=True, nullable=False, server_default=text("0"))
    dist_code = db.Column(INTEGER, primary_key=True, nullable=False, server_default=text("0"))
    state_id = db.Column(INTEGER, primary_key=True, nullable=False, server_default=text("0"))
    taluka_name = db.Column(VARCHAR(100), nullable=False)
    display = db.Column(VARCHAR(1), nullable=False, default='Y')
    create_modify = db.Column(TIMESTAMP, default=datetime.utcnow)

    def __repr__(self):
        return f"<Taluka {self.taluka_code} - {self.taluka_name}>"