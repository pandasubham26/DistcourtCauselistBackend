from datetime import datetime

from sqlalchemy import SMALLINT, VARCHAR, TIMESTAMP, INTEGER

from app.extensions import db


class JudgeCourtBaseTable(db.Model):
    __tablename__ = 'judge_t'
    __abstract__ = True
    __table_args__ = {'schema': 'public', 'extend_existing': True}

    court_no = db.Column(db.Integer, primary_key=True)
    judge_code = db.Column(db.Integer, primary_key=True)
    jocode = db.Column(db.String(8))
    desg_code = db.Column(db.Integer)
    from_dt = db.Column(db.Date, primary_key=True)
    to_dt = db.Column(db.Date)
    incharge = db.Column(db.String(1))
    est_code_src = db.Column(db.String(8), primary_key=True)
    display = db.Column(db.String(1))

    def to_dict(self):
        return {
            'court_no': self.court_no,
            'judge_code': self.judge_code,
            'desg_code': self.desg_code
        }