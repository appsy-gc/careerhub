from init import db, ma

class Partner(db.Model):
    __tablename__ = "cpartners"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    club = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(100), nullable=False, unique=True)

class PartnerSchema(ma.Schema):
    ordered=True
    class Meta:
        fields = ("id", "name", "club", "address", "email")

partner_schema = PartnerSchema()
partners_schema = PartnerSchema(many=True)