from flask.views import MethodView
from flask_smorest import Blueprint
from flask import jsonify, request, send_from_directory
from models import LandBoundary, User
from db import db
import os
import folium
from schemas import LandBoundarySchema, UserSchema

bp = Blueprint("land", __name__, url_prefix="/land", description="Operations on land boundaries")

# Folder to store generated map files
MAP_FOLDER = os.path.join(os.getcwd(), "maps")
if not os.path.exists(MAP_FOLDER):
    os.makedirs(MAP_FOLDER)


@bp.route("/boundaries")
class LandBoundaryList(MethodView):
    @bp.arguments(LandBoundarySchema)
    @bp.response(201, LandBoundarySchema)
    def post(self, data):
        """Add a land boundary for a user"""
        username = data.get("username")
        user = User.query.filter_by(username=username).first()
        if not user:
            bp.abort(404, message="User not found")

        # Save boundary in the database
        new_boundary = LandBoundary(user_id=user.id, boundary=data["boundary"])
        db.session.add(new_boundary)
        db.session.commit()

        # Generate a map with the polygon
        polygon_coords = data["boundary"]["coordinates"][0]  # Assuming GeoJSON format
        tunis_center = [34.0, 9.0]  # Approximate center of Tunisia
        m = folium.Map(location=tunis_center, zoom_start=7)
        folium.Polygon(
            locations=polygon_coords,
            color="blue",
            weight=2,
            fill=True,
            fill_opacity=0.4,
        ).add_to(m)

        # Save the map to an HTML file
        map_filename = f"map_{new_boundary.id}.html"
        map_path = os.path.join(MAP_FOLDER, map_filename)
        m.save(map_path)

        return {"message": "Land boundary added successfully", "map_link": f"/land/viewmap/{map_filename}"}, 201


@bp.route("/viewmap/<map_filename>")
class LandBoundaryMap(MethodView):
    @bp.response(200)
    def get(self, map_filename):
        """View a map by filename"""
        try:
            return send_from_directory(MAP_FOLDER, map_filename)
        except FileNotFoundError:
            bp.abort(404, message="Map not found")


@bp.route("/get-by-user/<int:user_id>")
class LandBoundaryByUser(MethodView):
    @bp.response(200, UserSchema)
    def get(self, user_id):
        """Get all land boundaries for a user"""
        user = User.query.get(user_id)
        if not user:
            bp.abort(404, message="User not found")

        lands = LandBoundary.query.filter_by(user_id=user_id).all()
        result = [{"id": land.id, "boundary": land.boundary} for land in lands]

        return {"user": {"id": user.id, "username": user.username}, "lands": result}
