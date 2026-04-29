from app.extensions import db


class DailyProcBaseTable(db.Model):
    __tablename__ = 'daily_proc'
    __abstract__ = True
    __table_args__ = {'schema': 'public', 'extend_existing': True}

    cino = db.Column(db.String, primary_key=True)
    purpose_code = db.Column(db.Integer)
    jocode = db.Column(db.Integer)
    todays_date = db.Column(db.Date)
    judge_code = db.Column(db.String)
    srno = db.Column(db.Integer)
    next_date = db.Column(db.Date)
    court_no = db.Column(db.Integer)