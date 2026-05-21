from app.extensions import db


class CivilTBaseTable(db.Model):
    __tablename__ = 'civil_t'
    __abstract__ = True
    __table_args__ = {'schema': 'public', 'extend_existing': True}

    cino = db.Column(db.String, primary_key=True)
    reg_no = db.Column(db.Integer)
    reg_year = db.Column(db.Integer)
    regcase_type = db.Column(db.String)
    filcase_type = db.Column(db.String)
    fil_no = db.Column(db.Integer)
    fil_year = db.Column(db.Integer)
    pet_name = db.Column(db.String)
    res_name = db.Column(db.String)
    pet_adv = db.Column(db.String)
    res_adv = db.Column(db.String)
    filing_no = db.Column(db.String)
    sr_no = db.Column(db.Integer)
    date_first_list = db.Column(db.Date)
    date_next_list = db.Column(db.Date)
    date_last_list = db.Column(db.Date)
    date_of_decision = db.Column(db.Date)
    court_no = db.Column(db.Integer)
    purpose_next = db.Column(db.Integer)