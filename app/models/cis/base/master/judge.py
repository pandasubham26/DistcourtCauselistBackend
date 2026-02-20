from datetime import datetime

from sqlalchemy import SMALLINT, VARCHAR, TIMESTAMP, INTEGER

from app.extensions import db


class JudgeNameBaseTable(db.Model):
    __tablename__ = 'judge_name_t'
    __abstract__ = True
    __table_args__ = {'schema': 'public', 'extend_existing': True}

    judge_code = db.Column(db.Integer, primary_key=True)
    judge_name = db.Column(db.String(100), nullable=False)
    display = db.Column(db.String(1), nullable=False)
    jto_dt = db.Column(db.Date)
    jfrom_dt = db.Column(db.Date)
    desg_code = db.Column(db.Integer)
    jocode = db.Column(db.String(10))
    create_modify = db.Column(db.TIMESTAMP, default=datetime.utcnow)
    est_code_src = db.Column(db.String(10))

    def to_dict(self):
        return {
            'judge_code': self.judge_code,
            'judge_name': self.judge_name,
            'est_code_src': self.est_code_src
        }