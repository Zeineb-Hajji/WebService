from db import db

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    role = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(200), nullable=False)
    land_boundaries = db.relationship('LandBoundary', backref='user', lazy=True)
class Region(db.Model):
    __tablename__ = 'regions'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    # Relationship with Deforestation
    deforestation_data = db.relationship('Deforestation', back_populates='region', cascade='all, delete-orphan')

class LandBoundary(db.Model):
    __tablename__ = 'land_boundaries'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)  # Foreign key to User table
    boundary = db.Column(db.JSON, nullable=False)  # GeoJSON data for the boundary

    def __repr__(self):
        return f"<LandBoundary id={self.id} user_id={self.user_id}>"

class Deforestation(db.Model):
    __tablename__ = 'deforestations'
    id = db.Column(db.Integer, primary_key=True)
    region_id = db.Column(db.Integer, db.ForeignKey('regions.id'), nullable=False)
    deforestation_trend = db.Column(db.String(200))
    co2_emission = db.Column(db.Float)
    # Relationship with Region
    region = db.relationship('Region', back_populates='deforestation_data')

