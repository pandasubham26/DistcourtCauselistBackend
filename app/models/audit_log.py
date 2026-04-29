from app.extensions import db
from datetime import datetime


class AuditLog(db.Model):
    __tablename__ = "audit_log"

    id = db.Column(db.Integer, primary_key=True)

    actor_user_id = db.Column(
        db.Integer,
        db.ForeignKey("users.id"),
        nullable=False
    )

    action = db.Column(
        db.String(255),
        nullable=False
    )

    entity = db.Column(
        db.String(255),
        nullable=True
    )

    entity_id = db.Column(
        db.String(255),
        nullable=True
    )

    details = db.Column(
        db.JSON,
        nullable=True
    )

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    def to_dict(self):
        return {
            "id": self.id,
            "actor_user_id": self.actor_user_id,
            "action": self.action,
            "entity": self.entity,
            "entity_id": self.entity_id,
            "details": self.details,
            "created_at": self.created_at.isoformat()
        }