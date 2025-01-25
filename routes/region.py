from flask.views import MethodView
from flask_smorest import Blueprint
from flask import request, jsonify,send_file
import matplotlib.pyplot as plt
import io 
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

# Extract vaccine names and stock levels
        region_names = [item.name for item in regions]
        risk_score = [item.risk_score for item in regions]

# Create the bar chart
        plt.figure(figsize=(10, 6))
        plt.bar(region_names,risk_score)
        plt.xlabel('Regions_names')
        plt.ylabel('Risk_score')
        plt.title('REGIONS_RISKSCORE')
        plt.xticks(rotation=45, ha="right")

# Save the chart to an in-memory file
        img = io.BytesIO()
        plt.tight_layout()
        plt.savefig(img, format='png')
        img.seek(0)

# Send the image as a response
        return send_file(img, mimetype='image/png', as_attachment=False, download_name='Regionschart.png')


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

