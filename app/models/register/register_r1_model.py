from app.extensions import db
from datetime import datetime

class RegisterRThirtyFour(db.Model):
    __tablename__ = "register_r34"

    id = db.Column(db.Integer, primary_key=True)
    court_name = db.Column(db.String(255), nullable=False)
    serial_no = db.Column(db.Integer, nullable=False)
    transferred = db.Column(db.String(255))
    order_ix = db.Column(db.String(255))
    otherwise = db.Column(db.String(255))
    without_days = db.Column(db.Integer)
    ex_parte = db.Column(db.String(255))
    award = db.Column(db.String(255))
    dismissal = db.Column(db.String(255))
    admission_days = db.Column(db.Integer)
    compromise = db.Column(db.String(255))
    compromise_days = db.Column(db.Integer)
    plaintiff = db.Column(db.String(255))
    defendant = db.Column(db.String(255))
    trial_days = db.Column(db.Integer)
    arbitration = db.Column(db.String(255))
    total_days = db.Column(db.Integer)
    remarks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "court_name": self.court_name,
            "serial_no": self.serial_no,
            "transferred": self.transferred,
            "order_ix": self.order_ix,
            "otherwise": self.otherwise,
            "without_days": self.without_days,
            "ex_parte": self.ex_parte,
            "award": self.award,
            "dismissal": self.dismissal,
            "admission_days": self.admission_days,
            "compromise": self.compromise,
            "compromise_days": self.compromise_days,
            "plaintiff": self.plaintiff,
            "defendant": self.defendant,
            "trial_days": self.trial_days,
            "arbitration": self.arbitration,
            "total_days": self.total_days,
            "remarks": self.remarks,
        }
    

class RegisterRTwenty(db.Model):
    __tablename__ = "register_r20"

    id = db.Column(db.Integer, primary_key=True)
    court_name = db.Column(db.String(255), nullable=False)
    consecutive_no = db.Column(db.Integer, nullable=False)
    case_number = db.Column(db.Integer, nullable=False)
    parties = db.Column(db.String(255), nullable=False)
    decision_date = db.Column(db.Date)
    file_details = db.Column(db.String(100))
    disposed_date = db.Column(db.Date)
    shelf_details = db.Column(db.String(250))
    remarks = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "court_name": self.court_name,
            "consecutive_no": self.consecutive_no,
            "case_number": self.case_number,
            "decision_date": str(self.decision_date) if self.decision_date else None,
            "parties": self.parties,
            "file_details": self.file_details,
            "disposed_date": str(self.disposed_date) if self.disposed_date else None,
            "shelf_details": self.shelf_details,
            "remarks": self.remarks,
        }


class RegisterROne(db.Model):
    __tablename__ = "register_r1"

    id = db.Column(db.Integer, primary_key=True)

    # Court Information
    court_name = db.Column(db.String(255), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer, nullable=False)

    # Suit Details
    presentation_date = db.Column(db.Date, nullable=False)
    serial_no = db.Column(db.String(100), nullable=False)
    suit_name = db.Column(db.String(255), nullable=False)
    casetype = db.Column(db.String(100), nullable=False)

    # Plaintiff Details
    plaintiff_name = db.Column(db.String(255), nullable=False)
    plaintiff_description = db.Column(db.Text)
    plaintiff_address = db.Column(db.Text)

    # Defendant Details
    defendant_name = db.Column(db.String(255), nullable=False)
    defendant_description = db.Column(db.Text)
    defendant_address = db.Column(db.Text)

    # Claim Details
    claim_value = db.Column(db.String(100))
    cause_of_action = db.Column(db.Text)
    remarks = db.Column(db.Text)

    # Judgment Details
    judgement_from_whom = db.Column(db.String(255))
    judgement_amount = db.Column(db.String(100))
    judgement_date = db.Column(db.Date)
    judgement_for_what = db.Column(db.Text)

    # Appeal Details
    appeal_date = db.Column(db.Date)
    appeal_against = db.Column(db.String(255))
    appeal_amount = db.Column(db.String(100))
    appeal_number_year = db.Column(db.String(255))
    appeal_order_details = db.Column(db.Text)

    # Adjustment Details
    adjustment_court = db.Column(db.String(255))
    adjustment_name = db.Column(db.String(255))
    adjustment_particulars = db.Column(db.Text)

    # Execution Details
    execution_date = db.Column(db.Date)
    serial_no_under_rule = db.Column(db.String(100))
    execution_application_details = db.Column(db.Text)
    execution_against_whom = db.Column(db.String(255))
    execution_for_what = db.Column(db.Text)

    # Financial Details
    costs_amount = db.Column(db.String(100))
    paid_into_court = db.Column(db.String(100))
    relief_amount_due = db.Column(db.String(100))

    # Additional Details
    person_detained = db.Column(db.String(255))
    return_minute = db.Column(db.Text)
    appeal_revision_orders = db.Column(db.Text)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            "id": self.id,
            "court_name": self.court_name,
            "location": self.location,
            "year": self.year,
            "presentation_date": str(self.presentation_date) if self.presentation_date else None,
            "serial_no": self.serial_no,
            "suit_name": self.suit_name,
            "casetype": self.casetype,
            "plaintiff_name": self.plaintiff_name,
            "defendant_name": self.defendant_name,
            "claim_value": self.claim_value,
            "judgement_amount": self.judgement_amount,
            "appeal_amount": self.appeal_amount,
            "relief_amount_due": self.relief_amount_due
        }