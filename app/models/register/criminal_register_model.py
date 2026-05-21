from datetime import datetime

from app.extensions import db


class CriminalRegisterROne(db.Model):
    __tablename__ = "criminal_register_r1"

    id = db.Column(db.Integer, primary_key=True)
    court_name = db.Column(db.String(255), nullable=False)
    estcode = db.Column(db.String(10), nullable=False)
    judge = db.Column(db.String(100), nullable=False)
    serial_no = db.Column(db.Integer, nullable=False)
    case_no = db.Column(db.Integer, nullable=False)
    case_year = db.Column(db.Integer, nullable=False)
    complaint_date = db.Column(db.Date, nullable=False)
    complainant_name = db.Column(db.String(100), nullable=False)
    accused_names = db.Column(db.String(255), nullable=False)
    nature_section = db.Column(db.Text)
    preliminary_order = db.Column(db.Text)
    final_order = db.Column(db.Text)
    remarks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "court_name": self.court_name,
            "estcode": self.estcode,
            "judge": self.judge,
            "complaint_date": str(self.complaint_date) if self.complaint_date else None,
            "serial_no": self.serial_no,
            "complainant_name": self.complainant_name,
            "accused_names": self.accused_names,
            "nature_section": self.nature_section,
            "preliminary_order": self.preliminary_order,
            "final_order": self.final_order,
            "remarks": self.remarks,
            "case_no": self.case_no,
            "case_year": self.case_year
        }


class CriminalRegisterRThree(db.Model):
    __tablename__ = "criminal_register_r3"

    id = db.Column(db.Integer, primary_key=True)
    court_name = db.Column(db.String(255), nullable=False)
    estcode = db.Column(db.String(10), nullable=False)
    judge = db.Column(db.String(100), nullable=False)
    serial_no = db.Column(db.Integer, nullable=False)
    case_no = db.Column(db.Integer, nullable=False)
    case_year = db.Column(db.Integer, nullable=False)
    date_of_institution = db.Column(db.Date, nullable=False)
    date_of_receipt = db.Column(db.Date, nullable=False)
    complainant_name = db.Column(db.String(100), nullable=False)
    accused_count = db.Column(db.Integer, nullable=False)
    nature_section = db.Column(db.Text)
    final_order_date = db.Column(db.Text)
    appeal_revision_result = db.Column(db.Text)
    remarks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "court_name": self.court_name,
            "estcode": self.estcode,
            "judge": self.judge,
            "serial_no": self.serial_no,
            "date_of_institution": self.date_of_institution,
            "date_of_receipt": self.date_of_receipt,
            "complainant_name": self.complainant_name,
            "accused_count": self.accused_count,
            "nature_section": self.nature_section,
            "final_order_date": self.final_order_date,
            "appeal_revision_result": self.appeal_revision_result,
            "remarks": self.remarks,
            "case_no": self.case_no,
            "case_year": self.case_year
        }