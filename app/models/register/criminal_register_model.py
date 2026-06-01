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


class CriminalRegisterREight(db.Model):
    __tablename__ = "criminal_register_r8"

    id = db.Column(db.Integer, primary_key=True)
    serial_no = db.Column(db.Integer, nullable=False)
    witness_name = db.Column(db.String(255), nullable=False)
    case_number = db.Column(db.String(100), nullable=False)
    est_code = db.Column(db.String(10), nullable=False)
    judge = db.Column(db.String(100), nullable=False)
    attendance_day_1 = db.Column(db.Date)
    attendance_day_2 = db.Column(db.Date)
    attendance_day_3 = db.Column(db.Date)
    attendance_day_4 = db.Column(db.Date)
    attendance_day_5 = db.Column(db.Date)
    attendance_day_6 = db.Column(db.Date)
    discharged_day_1 = db.Column(db.Date)
    discharged_day_2 = db.Column(db.Date)
    discharged_day_3 = db.Column(db.Date)
    discharged_after_day_3 = db.Column(db.Date)
    examined = db.Column(db.String(50))
    cross_examination_declined = db.Column(db.String(50))
    not_examined = db.Column(db.String(50))
    presiding_officer_initial = db.Column(db.String(100))
    remarks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "serial_no": self.serial_no,
            "witness_name": self.witness_name,
            "case_number": self.case_number,
            "attendance_day_1": str(self.attendance_day_1) if self.attendance_day_1 else None,
            "attendance_day_2": str(self.attendance_day_2) if self.attendance_day_2 else None,
            "attendance_day_3": str(self.attendance_day_3) if self.attendance_day_3 else None,
            "attendance_day_4": str(self.attendance_day_4) if self.attendance_day_4 else None,
            "attendance_day_5": str(self.attendance_day_5) if self.attendance_day_5 else None,
            "attendance_day_6": str(self.attendance_day_6) if self.attendance_day_6 else None,
            "discharged_day_1": str(self.discharged_day_1) if self.discharged_day_1 else None,
            "discharged_day_2": str(self.discharged_day_2) if self.discharged_day_2 else None,
            "discharged_day_3": str(self.discharged_day_3) if self.discharged_day_3 else None,
            "discharged_after_day_3": str(self.discharged_after_day_3) if self.discharged_after_day_3 else None,
            "examined": self.examined,
            "cross_examination_declined": self.cross_examination_declined,
            "not_examined": self.not_examined,
            "presiding_officer_initial": self.presiding_officer_initial,
            "remarks": self.remarks,
        }


class CriminalRegisterRThirteen(db.Model):
    __tablename__ = "criminal_register_r13"

    id = db.Column(db.Integer, primary_key=True)
    est_code = db.Column(db.String(10), nullable=False)
    court_name = db.Column(db.String(100), nullable=False)
    primary_case_no = db.Column(db.String(100), nullable=False)
    magistrate_name = db.Column(db.String(255), nullable=False)
    trial_case_no_year = db.Column(db.String(100), nullable=False)
    complainant_name = db.Column(db.String(255))
    accused_name = db.Column(db.String(255))
    final_order_details = db.Column(db.Text)
    appeal_revision_result = db.Column(db.Text)
    file_class = db.Column(db.String(100))
    disposed_shelved_date = db.Column(db.Date)
    shelf_rack_no = db.Column(db.String(100))
    destruction_date = db.Column(db.Date)
    remarks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "est_code": self.est_code,
            "court_name": self.court_name,
            "primary_case_no": self.primary_case_no,
            "magistrate_name": self.magistrate_name,
            "trial_case_no_year": self.trial_case_no_year,
            "complainant_name": self.complainant_name,
            "accused_name": self.accused_name,
            "final_order_details": self.final_order_details,
            "appeal_revision_result": self.appeal_revision_result,
            "file_class": self.file_class,
            "disposed_shelved_date": str(self.disposed_shelved_date) if self.disposed_shelved_date else None,
            "shelf_rack_no": self.shelf_rack_no,
            "destruction_date": str(self.destruction_date) if self.destruction_date else None,
            "remarks": self.remarks
        }