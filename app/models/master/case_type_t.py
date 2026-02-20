from datetime import datetime

from sqlalchemy.dialects.postgresql import SMALLINT, VARCHAR, TIMESTAMP, INTEGER

from app.extensions import db


class CaseTypeT(db.Model):
    __tablename__ = 'case_type_t'
    __table_args__ = {'schema': 'public'}

    case_type = db.Column(SMALLINT, primary_key=True, default=0)
    type_name = db.Column(VARCHAR(50))
    full_form = db.Column(VARCHAR(100))
    type_flag = db.Column(INTEGER, nullable=False, default='1')
    display = db.Column(VARCHAR(1), nullable=False, default='Y')
    create_modify = db.Column(TIMESTAMP, default=datetime.utcnow)


    def __repr__(self):
        return f"<CaseType {self.case_type} - {self.type_name}>"

    def to_dict(self):
        return {
            "case_type": self.case_type,
            "type_name": self.type_name,
            "full_form": self.full_form,
            "type_flag": self.type_flag,
            "display": self.display,
            "create_modify": self.create_modify
        }
