from flask import Blueprint, request
from init import db

from models.cpartners import Partner, PartnerSchema

partners_bp = Blueprint("partners", __name__, url_prefix="/partners")

# Read all - /partners - GET
@partners_bp.route("/")
def get_partners():
    # Get the club from browser link /partners?club=club
    club = request.args.get("club")
    # If a club is given, filter by club
    if club:
        stmt = db.select(Partner).filter_by(club=club).order_by(Partner.id)
    else:
        stmt = db.select(Partner).order_by(Partner.id)

    partner_list = db.session.scalars(stmt)
    return PartnerSchema(many=True).dump(partner_list)

# Read one - /partner/id - GET
@partners_bp.route("/<int:partner_id>")
def get_partner(partner_id):
    stmt = db.select(Partner).filter_by(id=partner_id)
    partner = db.session.scalar(stmt)
    if partner:
        return PartnerSchema().dump(partner)
    else:
        return {"message": f"Partner with id '{partner_id}' does not exist"}, 404

# Create - /partners - POST


# Update - /partner/id - PUT or PATCH


# Delete - /partner/id - DELETE
