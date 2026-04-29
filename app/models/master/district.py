from datetime import datetime

from sqlalchemy.dialects.postgresql import SMALLINT, VARCHAR, TIMESTAMP, INTEGER

from app.extensions import db


class District(db.Model):
    __tablename__ = 'district_t'
    __table_args__ = {'schema': 'public'}

    dist_code = db.Column(SMALLINT, primary_key=True)
    state_id = db.Column(INTEGER)
    dist_name = db.Column(VARCHAR(50))
    display = db.Column(VARCHAR(1), nullable=False, default='Y')
    create_modify = db.Column(TIMESTAMP, default=datetime.utcnow)

    def __repr__(self):
        return f"<State {self.state_id} - {self.state}>"

