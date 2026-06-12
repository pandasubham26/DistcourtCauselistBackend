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
    accused_count = db.Column(db.String(100), nullable=False)
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


class CriminalRegisterRSeven(db.Model):
    __tablename__ = "criminal_register_r7"

    id = db.Column(db.Integer, primary_key=True, index=True)
    serial_no = db.Column(db.Integer, nullable=False)
    nature_of_documents = db.Column(db.String(255), nullable=False)
    date = db.Column(db.Date, nullable=False)
    case_number = db.Column(db.String(100), nullable=False)
    est_code = db.Column(db.String(20), nullable=False)
    judge = db.Column(db.String(255), nullable=False)
    court_name = db.Column(db.String(255), nullable=False)
    process_fee_rs = db.Column(db.Integer, default=0)
    process_fee_ps = db.Column(db.Integer, default=0)
    affidavit_fee_rs = db.Column(db.Integer, default=0)
    affidavit_fee_ps = db.Column(db.Integer, default=0)
    other_fee_rs = db.Column(db.Integer, default=0)
    other_fee_ps = db.Column(db.Integer, default=0)
    remarks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "est_code": self.est_code,
            "court_name": self.court_name,
            "nature_of_documents": self.nature_of_documents,
            "affidavit_fee_ps": self.affidavit_fee_ps,
            "case_number": self.case_number,
            "serial_no": self.serial_no,
            "judge": self.judge,
            "process_fee_rs": self.process_fee_rs,
            "process_fee_ps": self.process_fee_ps,
            "affidavit_fee_rs": self.affidavit_fee_rs,
            "date": str(self.date) if self.date else None,
            "other_fee_rs": self.other_fee_rs,
            "other_fee_ps": self.other_fee_ps,
            "remarks": self.remarks
        }


class CriminalRegisterRTwo(db.Model):
    __tablename__ = "criminal_register_r2"

    id = db.Column(db.Integer, primary_key=True)
    court_name = db.Column(db.String(255), nullable=False)
    case_no = db.Column(db.String(100), nullable=False)
    auth_estcode = db.Column(db.String(20), nullable=False)
    auth_judge = db.Column(db.String(255), nullable=False)
    serial_no = db.Column(db.Integer, nullable=False)
    police_station = db.Column(db.String(255), nullable=False)
    receipt_date = db.Column(db.Date, nullable=False)
    crime_information = db.Column(db.Text, nullable=False)
    party_names = db.Column(db.Text, nullable=False)
    police_investigation_return = db.Column(db.Text, nullable=False)
    preliminary_order = db.Column(db.Text, nullable=False)
    final_order = db.Column(db.Text, nullable=False)
    remarks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "court_name": self.court_name,
            "case_no": self.case_no,
            "auth_estcode": self.auth_estcode,
            "auth_judge": self.auth_judge,
            "serial_no": self.serial_no,
            "police_station": self.police_station,
            "receipt_date": self.receipt_date.isoformat() if self.receipt_date else None,
            "crime_information": self.crime_information,
            "party_names": self.party_names,
            "police_investigation_return": self.police_investigation_return,
            "preliminary_order": self.preliminary_order,
            "final_order": self.final_order,
            "remarks": self.remarks,
            "created_at": self.created_at.isoformat() if self.created_at else None,
        }


class CriminalRegisterRNineA(db.Model):
    __tablename__ = "criminal_register_r9a"

    id = db.Column(db.Integer, primary_key=True)
    auth_estcode = db.Column(db.String(20), nullable=False)
    auth_judge = db.Column(db.String(200), nullable=False)
    court_name = db.Column(db.String(255), nullable=False)
    serial_no = db.Column(db.Integer, nullable=False)
    case_no = db.Column(db.String(100), nullable=False)
    person_name = db.Column(db.String(255), nullable=False)
    nature_of_process = db.Column(db.String(255), nullable=False)
    issue_date = db.Column(db.Date, nullable=False)
    returnable_date = db.Column(db.Date, nullable=False)
    receiver_date = db.Column(db.Date, nullable=False)
    return_date = db.Column(db.Date, nullable=True)
    remarks = db.Column(db.Text, nullable=True)
    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    def to_dict(self):
        return {
            "id": self.id,
            "auth_estcode": self.auth_estcode,
            "auth_judge": self.auth_judge,
            "court_name": self.court_name,
            "serial_no": self.serial_no,
            "case_no": self.case_no,
            "person_name": self.person_name,
            "nature_of_process": self.nature_of_process,
            "issue_date": self.issue_date.strftime("%Y-%m-%d") if self.issue_date else None,
            "returnable_date": self.returnable_date.strftime("%Y-%m-%d") if self.returnable_date else None,
            "receiver_date": self.receiver_date.strftime("%Y-%m-%d") if self.receiver_date else None,
            "return_date": self.return_date.strftime("%Y-%m-%d") if self.return_date else None,
            "remarks": self.remarks,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }


class CriminalRegisterRTenA(db.Model):
    __tablename__ = "criminal_register_r10a"

    id = db.Column(db.Integer, primary_key=True)
    auth_estcode = db.Column(db.String(20), nullable=False)
    auth_judge = db.Column(db.String(200), nullable=False)
    court_name = db.Column(db.String(255), nullable=False)
    serial_no = db.Column(db.Integer, nullable=False)
    case_no = db.Column(db.String(100), nullable=False)
    trail_date = db.Column(db.Date, nullable=False)
    prosecution_witnesses = db.Column(db.Text, nullable=False)
    issue_date = db.Column(db.Date, nullable=False)
    mode_of_service = db.Column(db.String(255), nullable=False)
    return_date = db.Column(db.Date, nullable=False)
    suf_insuff = db.Column(db.String(100), nullable=False)
    step_taken = db.Column(db.Text, nullable=True)
    remarks = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "auth_estcode": self.auth_estcode,
            "auth_judge": self.auth_judge,
            "court_name": self.court_name,
            "serial_no": self.serial_no,
            "case_no": self.case_no,
            "trail_date": self.trail_date.strftime("%Y-%m-%d") if self.trail_date else None,
            "prosecution_witnesses": self.prosecution_witnesses,
            "issue_date": self.issue_date.strftime("%Y-%m-%d") if self.issue_date else None,
            "mode_of_service": self.mode_of_service,
            "return_date": self.return_date.strftime("%Y-%m-%d") if self.return_date else None,
            "suf_insuff": self.suf_insuff,
            "step_taken": self.step_taken,
            "remarks": self.remarks,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }


class CriminalRegisterRThirteenA(db.Model):
    __tablename__ = "criminal_register_r13a"

    id = db.Column(db.Integer, primary_key=True)

    auth_estcode = db.Column(db.String(20), nullable=False)
    auth_judge = db.Column(db.String(200), nullable=False)

    court_name = db.Column(db.String(255), nullable=False)
    serial_no = db.Column(db.Integer, nullable=False)
    case_no = db.Column(db.String(100), nullable=False)

    parties_name = db.Column(db.Text, nullable=False)
    dormant_order_date = db.Column(db.Date, nullable=False)
    record_room_received_date = db.Column(db.Date, nullable=False)
    shelf_rack_no = db.Column(db.String(100), nullable=False)

    requisition_received_date = db.Column(db.Date, nullable=True)
    trial_court_sent_date = db.Column(db.Date, nullable=True)

    remarks = db.Column(db.Text, nullable=True)

    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "auth_estcode": self.auth_estcode,
            "auth_judge": self.auth_judge,
            "court_name": self.court_name,
            "serial_no": self.serial_no,
            "case_no": self.case_no,
            "parties_name": self.parties_name,
            "dormant_order_date": self.dormant_order_date.strftime("%Y-%m-%d") if self.dormant_order_date else None,
            "record_room_received_date": self.record_room_received_date.strftime("%Y-%m-%d") if self.record_room_received_date else None,
            "shelf_rack_no": self.shelf_rack_no,
            "requisition_received_date": self.requisition_received_date.strftime("%Y-%m-%d") if self.requisition_received_date else None,
            "trial_court_sent_date": self.trial_court_sent_date.strftime("%Y-%m-%d") if self.trial_court_sent_date else None,
            "remarks": self.remarks,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S"),
        }