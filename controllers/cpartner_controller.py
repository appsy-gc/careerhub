from flask import Blueprint, request, jsonify, Response
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

        if isinstance(body_data, list):
            new_partners = []
            for entry in body_data:
            # Create partner instance
                new_partner = Partner(
                    name = entry.get("name", "TBC"),
                    club = entry.get("club", "TBC"),
                    address = entry.get("address", "TBC"),
                    email = entry.get("email", "TBC")
                )
                new_partners.append(new_partner)

            # Add multiple partners
            db.session.add_all(new_partners)
            # Commit
            db.session.commit()

            return jsonify(PartnerSchema().dump(new_partners)), 201
        
        # Single record creation
        new_partner = Partner(
            name=body_data.get("name", "TBC"),
            club=body_data.get("club", "TBC"),
            address=body_data.get("address", "TBC"),
            email=body_data.get("email", "TBC"),
        )

        # Add the single partner
        db.session.add(new_partner)
        db.session.commit()

        # Return the created partner
        return PartnerSchema().dump(new_partner), 201

    except IntegrityError as err:
        print(err.orig.pgcode)
        if err.orig.pgcode == errorcodes.NOT_NULL_VIOLATION:
            # not_null_violation
            # Return specific field that is in violation
            return {"message": f"The field '{err.orig.diag.column_name}' is required"}, 409
        if err.orig.pgcode == errorcodes.UNIQUE_VIOLATION:
            return {"message": "Data already exists. Update partner details instead"}, 409

# Update - /partner/id - PUT or PATCH
@partners_bp.route("/<int:partner_id>", methods=["PUT", "PATCH"])
def update_partner(partner_id):
    stmt = db.select(Partner).filter_by(id=partner_id)
    partner = db.session.scalar(stmt)
    body_data = request.get_json()

    if partner:
        partner.name = body_data.get("name") or partner.name
        partner.club = body_data.get("club") or partner.club
        partner.address = body_data.get("address") or partner.address
        partner.email = body_data.get("email") or partner.email
        db.session.commit()
        return PartnerSchema().dump(partner)
    else:
        return {"message": f"Partner with id: '{partner_id}' does not exist"}, 404

# Delete - /partner/id - DELETE
@partners_bp.route("/<int:partner_id>", methods=["DELETE"])
def delete_partner(partner_id):
    stmt = db.select(Partner).filter_by(id=partner_id)
    partner = db.session.scalar(stmt)

    if partner:
        db.session.delete(partner)
        db.session.commit()
        return {"message": f"Partner: '{partner.name}' successfuly deleted"}
    else:
        return {"message": f"Partner with id: '{partner_id} does not exist"}, 404
    

#
