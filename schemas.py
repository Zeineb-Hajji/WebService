from marshmallow import Schema, fields

class RegionSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)
    risk_score=fields.Float(required=True)
class DeforestationSchema(Schema):
    id = fields.Int(dump_only=True)
    region_id = fields.Int(required=True)
    deforestation_trend = fields.Str(required=True)
    co2_emission = fields.Float(required=True)
    region_name = fields.Str(load_only=True)  
    region = fields.Nested("RegionSchema", dump_only=True)
    class Meta:
        schema_name = "DeforestationData" 

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    age = fields.Int(required=True)
    email = fields.Email(required=True)
    role = fields.Str(required=True)
    password = fields.Str(load_only=True)  
    class Meta:
        schema_name = "UserAccount"

class LandBoundarySchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    username = fields.Str(load_only=True)  
    boundary = fields.Dict(required=True)  
class ThreatSchema(Schema):
    id = fields.Int(dump_only=True)
    region_id = fields.Int(required=True)  # Foreign key to Region
    co2_emissions = fields.Float(required=True)  # CO2 emission in tons
    biodiversity_loss = fields.Str(required=True)  # e.g., "High", "Medium"
    soil_degradation = fields.Str(required=True)  # e.g., "Severe", "Mild"
    region = fields.Nested("RegionSchema", dump_only=True)  # Nested output
    class Meta:
        schema_name = "ThreatData"

# Recommendation Schema
class RecommendationSchema(Schema):
    id = fields.Int(dump_only=True)
    region_id = fields.Int(required=True)  # Foreign key to Region
    threat_type = fields.Str(required=True)  # e.g., "CO2", "Biodiversity"
    recommendation = fields.Str(required=True)  # Detailed recommendation
    region = fields.Nested("RegionSchema", dump_only=True)  # Nested output
    class Meta:
        schema_name = "RecommendationData"
