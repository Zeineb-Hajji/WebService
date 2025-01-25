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
    risk_score=db.Column(db.Float,nullable=True)
    deforestation_data = db.relationship('Deforestation', back_populates='region', cascade='all, delete-orphan')
    threats = db.relationship('Threat', back_populates='threats_region', cascade='all, delete-orphan')
    recommendations = db.relationship('Recommendation', back_populates='recommendations_region', cascade='all, delete-orphan')
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
    
    region = db.relationship('Region', back_populates='deforestation_data')
class Threat(db.Model):
    __tablename__ = 'threats'
    id = db.Column(db.Integer, primary_key=True)
    region_id = db.Column(db.Integer, db.ForeignKey('regions.id'), nullable=False)
    co2_emissions = db.Column(db.Float, nullable=False)  # Annual CO2 emissions in tons
    biodiversity_loss = db.Column(db.String(50), nullable=False)  # Biodiversity loss level
    soil_degradation = db.Column(db.String(50), nullable=False)
    threats_region = db.relationship('Region', back_populates='threats')
class Recommendation(db.Model):
    __tablename__ = 'recommendations'
    id = db.Column(db.Integer, primary_key=True)
    region_id = db.Column(db.Integer, db.ForeignKey('regions.id'), nullable=False)
    threat_type = db.Column(db.String(50), nullable=False)  # Type of threat (e.g., CO2, Biodiversity)
    recommendation = db.Column(db.Text, nullable=False)  # Mitigation strategy
    recommendations_region = db.relationship('Region', back_populates='recommendations')
  
