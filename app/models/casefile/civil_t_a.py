from app.extensions import db


class CivilTA(db.Model):
    __tablename__ = 'civil_t_a'

    cino = db.Column(db.String, primary_key=True)
    reg_no = db.Column(db.String)
    reg_year = db.Column(db.Integer)
    regcase_type = db.Column(db.String)
    pet_name = db.Column(db.String)
    res_name = db.Column(db.String)
    pet_adv = db.Column(db.String)
    res_adv = db.Column(db.String)