from flask.views import MethodView
from flask_smorest import Blueprint
from db import db
from models import Deforestation, Region
from schemas import DeforestationSchema

bp = Blueprint("deforestation", __name__, url_prefix="/deforestation", description="Operations on deforestation data")


@bp.route("/")
class DeforestationList(MethodView):
    @bp.response(200, DeforestationSchema(many=True))
    def get(self):
        """Get all deforestation data"""
        deforestation_data = Deforestation.query.all()
        return deforestation_data

    @bp.arguments(DeforestationSchema)
    @bp.response(201, DeforestationSchema)
    def post(self, data):
        """Add deforestation data"""
        region = Region.query.filter_by(name=data["region_name"]).first()
        if not region:
            bp.abort(404, message="Region not found")
        deforestation = Deforestation(region_id=region.id, **data)
        db.session.add(deforestation)
        db.session.commit()
        return deforestation


@bp.route("/<int:region_id>")
class DeforestationDetail(MethodView):
    @bp.response(200, DeforestationSchema)
    def get(self, region_id):
        """Get deforestation data for a specific region"""
        deforestation = Deforestation.query.filter_by(region_id=region_id).first()
        if not deforestation:
            bp.abort(404, message="Deforestation data not found")
        return deforestation

    @bp.arguments(DeforestationSchema(partial=True))
    @bp.response(200, DeforestationSchema)
    def put(self, data, region_id):
        """Update deforestation data for a specific region"""
        deforestation = Deforestation.query.filter_by(region_id=region_id).first()
        if not deforestation:
            bp.abort(404, message="Deforestation data not found")
        for key, value in data.items():
            setattr(deforestation, key, value)
        db.session.commit()
        return deforestation

