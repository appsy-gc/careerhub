from init import db, ma
from sqlalchemy import CheckConstraint

class Partner(db.Model):
    __tablename__ = "cpartners"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    club = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)
    __table_args__ = (
        CheckConstraint("email LIKE '%@%'", name='check_email_format')
    )

class PartnerSchema(ma.Schema):
    class Meta:
        fields = ("id", "name", "club", "address", "email")

partner_schema = PartnerSchema()
partners_schema = PartnerSchema(many=True)