from flask import Blueprint, request
from init import db
from sqlalchemy.exc import IntegrityError
from psycopg2 import errorcodes

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
@partners_bp.route("/", methods=["POST"])
def create_partner():
    # Exception handling for error
    try:
        # Get information from request body
        body_data = request.get_json()
        # Create partner instance
        new_partner = Partner(
            name = body_data.get("name"),
            club = body_data.get("club"),
            address = body_data.get("address"),
            email = body_data.get("email")
        )
        # Add
        db.session.add(new_partner)
        # Commit
        db.session.commit()
        return PartnerSchema().dump(new_partner), 201
    except IntegrityError as err:
        print(err.orig.pgcode)
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            # not_null_violation
            # Return specific field that is in violation
            return {"message": f"The field '{err.orig.diag.column_name}' is required"}, 409
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"message": "Data already exists. Update course details instead"}, 409

# Update - /partner/id - PUT or PATCH


# Delete - /partner/id - DELETE
