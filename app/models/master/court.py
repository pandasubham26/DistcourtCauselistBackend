from datetime import datetime

from sqlalchemy.dialects.postgresql import VARCHAR, TIMESTAMP

from app.extensions import db


class CourtName(db.Model):
    __tablename__ = 'court_name'
    __table_args__ = {'schema': 'public'}

    est_code = db.Column(VARCHAR(6), primary_key=True)
    court_name = db.Column(VARCHAR(50))
    state = db.Column(VARCHAR(50))
    district = db.Column(VARCHAR(50))
    create_modify = db.Column(TIMESTAMP, default=datetime.utcnow)

    def __repr__(self):
        return f"<Court {self.est_code} - {self.court_name}>"
