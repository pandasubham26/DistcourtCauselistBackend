from app.extensions import db


class PurposeT(db.Model):
    __tablename__ = 'purpose_t'

    purpose_code = db.Column(db.Integer, primary_key=True)
    purpose_name = db.Column(db.String)
    purpose_priority = db.Column(db.Integer)
    display = db.Column(db.String)