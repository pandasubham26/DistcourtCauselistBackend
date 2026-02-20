from app.extensions import db
from sqlalchemy.sql import func


class CaseFileHeader(db.Model):
    __tablename__ = 'casefile_header'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    barcode = db.Column(db.String(50), nullable=False)
    cino = db.Column(db.String(16))
    court = db.Column(db.String(50))
    judge = db.Column(db.String(50))
    est_code = db.Column(db.String(50))
    cis_case_type = db.Column(db.String(50), nullable=False)
    reg_case_type = db.Column(db.String(50), nullable=False)
    cis_case_no = db.Column(db.Integer, nullable=False)
    reg_case_no = db.Column(db.Integer, nullable=False)
    cis_case_year = db.Column(db.Integer, nullable=False)
    reg_case_year = db.Column(db.Integer, nullable=False)
    pet_name = db.Column(db.String(100))
    pet_adv = db.Column(db.String(100))
    res_name = db.Column(db.String(100))
    res_adv = db.Column(db.String(100))
    status = db.Column(db.String(20), default='Pending')
    display = db.Column(db.String(1), default='Y')
    uploaded_by = db.Column(db.String(100))
    uploaded_at = db.Column(db.DateTime, server_default=func.now())

    # Relationship → One Header : Many Detail
    details = db.relationship("CaseFileDetail", backref="header", cascade="all, delete-orphan")

    def to_dict(self):
        return {
            'id': self.id,
            'barcode': self.barcode,
            'cino': self.cino,
            'court': self.court,
            'judge': self.judge,
            'est_code': self.est_code,
            'cis_case_type': self.cis_case_type,
            'reg_case_type': self.reg_case_type,
            'cis_case_no': self.cis_case_no,
            'reg_case_no': self.reg_case_no,
            'cis_case_year': self.cis_case_year,
            'reg_case_year': self.reg_case_year,
            'pet_name': self.pet_name,
            'pet_adv': self.pet_adv,
            'res_name': self.res_name,
            'res_adv': self.res_adv,
            'uploaded_by': self.uploaded_by,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None,
            'details': [d.to_dict() for d in self.details]  # include detail list
        }


class CaseFileDetail(db.Model):
    __tablename__ = 'casefile_detail'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    casefile_id = db.Column(db.Integer, db.ForeignKey('casefile_header.id'), nullable=False)
    bulk_no = db.Column(db.String(50), nullable=False)
    file_path = db.Column(db.String(255), nullable=False)
    pages = db.Column(db.Integer, default=0)
    uploaded_by = db.Column(db.String(100))
    uploaded_at = db.Column(db.DateTime, server_default=func.now())

    def to_dict(self):
        return {
            'id': self.id,
            'casefile_id': self.casefile_id,
            'bulk_no': self.bulk_no,
            'file_path': self.file_path,
            'pages': self.pages,
            'uploaded_by': self.uploaded_by,
            'uploaded_at': self.uploaded_at.isoformat() if self.uploaded_at else None
        }
