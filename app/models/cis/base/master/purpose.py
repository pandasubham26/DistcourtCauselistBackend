from app.extensions import db


class PurposeTBaseTable(db.Model):
    __tablename__ = 'purpose_t'
    __abstract__ = True
    __table_args__ = {'schema': 'public', 'extend_existing': True}

    purpose_code = db.Column(db.Integer, primary_key=True)
    purpose_name = db.Column(db.String)
    purpose_priority = db.Column(db.Integer)
    display = db.Column(db.String)