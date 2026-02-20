from datetime import datetime
from sqlalchemy import INTEGER, VARCHAR, CHAR, DATE, TIMESTAMP
from app.extensions import db


class JudgeWithCourtNo(db.Model):
    __tablename__ = 'judge_t'
    __table_args__ = {'schema': 'public'}

    court_no = db.Column(INTEGER, primary_key=True)
    judge_code = db.Column(INTEGER, primary_key=True)
    jocode = db.Column(VARCHAR(8))
    desg_code = db.Column(INTEGER)
    from_dt = db.Column(DATE, primary_key=True)
    to_dt = db.Column(DATE)
    incharge = db.Column(CHAR(1))
    est_code_src = db.Column(VARCHAR(8), primary_key=True)
    display = db.Column(CHAR(1))
    create_modify = db.Column(TIMESTAMP, default=datetime.utcnow)

    def __repr__(self):
        return f"<Judge court_no={self.court_no}, judge_code={self.judge_code}, from_dt={self.from_dt}>"