from datetime import datetime

from sqlalchemy.dialects.postgresql import TIMESTAMP, VARCHAR, INTEGER

from app.extensions import db

class DesignationName(db.Model):
    __tablename__ = 'desg_t'
    __table_args__ = {'schema': 'public'}

    desgcode = db.Column(INTEGER, primary_key=True)
    desgname = db.Column(VARCHAR(100), nullable=False)
    display = db.Column(VARCHAR(1), nullable=False, default='Y')
    create_modify = db.Column(TIMESTAMP, default=datetime.utcnow)

    def __repr__(self):
        return f"<Designation {self.desgcode} - {self.desgname}>"