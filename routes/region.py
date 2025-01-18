from flask.views import MethodView
from flask_smorest import Blueprint
from flask import request, jsonify
from db import db
from models import Region
from schemas import RegionSchema

bp = Blueprint("region", __name__, url_prefix="/region", description="Operations on regions")

@bp.route("/")
class RegionList(MethodView):
    @bp.response(200, RegionSchema(many=True))
    def get(self):
        """Get all regions"""
        regions = Region.query.all()
        return regions

    @bp.arguments(RegionSchema)
    @bp.response(201, RegionSchema)
    def post(self, data):
        """Add a new region"""
        region = Region(**data)
        db.session.add(region)
        db.session.commit()
        return region


@bp.route("/<int:region_id>")
class RegionDetail(MethodView):
    @bp.response(200, RegionSchema)
    def get(self, region_id):
        """Get a region by ID"""
        region = Region.query.get_or_404(region_id)
        return region

    @bp.response(204)
    def delete(self, region_id):
        """Delete a region by ID"""
        region = Region.query.get_or_404(region_id)
        db.session.delete(region)
        db.session.commit()

