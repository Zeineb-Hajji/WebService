from flask.views import MethodView
from flask_smorest import Blueprint
from werkzeug.security import generate_password_hash
from models import User
from db import db
from schemas import UserSchema
from flask_jwt_extended import JWTManager

bp = Blueprint("auth", __name__, url_prefix="/auth", description="User authentication and management")


@bp.route("/register")
class RegisterUser(MethodView):
    @bp.arguments(UserSchema)
    @bp.response(201, UserSchema)
    def post(self, data):
        """Register a new user"""
        hashed_password = generate_password_hash(data["password"])
        user = User(
            username=data["username"],
            age=data["age"],
            email=data["email"],
            role=data["role"],
            password=hashed_password,
        )
        db.session.add(user)
        db.session.commit()
        return user


@bp.route("/users")
class UserList(MethodView):
    @bp.response(200, UserSchema(many=True))
    def get(self):
        """Get a list of all users"""
        users = User.query.all()
        return users


@bp.route("/users/<int:user_id>")
class UserDetail(MethodView):
    @bp.response(200, UserSchema)
    def get(self, user_id):
        """Get a user by ID"""
        user = User.query.get_or_404(user_id)
        return user

    @bp.arguments(UserSchema(partial=True))
    @bp.response(200, UserSchema)
    def put(self, data, user_id):
        """Update a user by ID"""
        user = User.query.get_or_404(user_id)
        for key, value in data.items():
            if key == "password":
                value = generate_password_hash(value)
            setattr(user, key, value)
        db.session.commit()
        return user

    @bp.response(204)
    def delete(self, user_id):
        """Delete a user by ID"""
        user = User.query.get_or_404(user_id)
        db.session.delete(user)
        db.session.commit()
