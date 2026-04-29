from sqlalchemy import func

from app.extensions import db

class CauseList(db.Model):
    __tablename__ = 'causelist'

    id = db.Column(db.Integer, primary_key=True)
    srno = db.Column(db.Integer)
    date = db.Column(db.String(20), nullable=False)
    next_date = db.Column(db.String(20), nullable=True)
    judge_name = db.Column(db.String(100), nullable=False)
    bench = db.Column(db.String(25))
    type_flag = db.Column(db.Integer)
    casetype = db.Column(db.String(40))
    casenumber = db.Column(db.Integer)
    caseyear = db.Column(db.Integer)
    purposename = db.Column(db.String(100))
    purpose_priority = db.Column(db.Integer)
    petname = db.Column(db.String(100))
    resname = db.Column(db.String(100))
    petadv = db.Column(db.String(100))
    resadv = db.Column(db.String(100))
    created_at = db.Column(db.DateTime(timezone=True), server_default=func.now())