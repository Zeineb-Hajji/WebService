from marshmallow import Schema, fields

class RegionSchema(Schema):
    id = fields.Int(dump_only=True)
    name = fields.Str(required=True)

class DeforestationSchema(Schema):
    id = fields.Int(dump_only=True)
    region_id = fields.Int(required=True)
    deforestation_trend = fields.Str(required=True)
    co2_emission = fields.Float(required=True)
    region_name = fields.Str(load_only=True)  # Used for input only
    region = fields.Nested("RegionSchema", dump_only=True)
    class Meta:
        schema_name = "DeforestationData" 

class UserSchema(Schema):
    id = fields.Int(dump_only=True)
    username = fields.Str(required=True)
    age = fields.Int(required=True)
    email = fields.Email(required=True)
    role = fields.Str(required=True)
    password = fields.Str(load_only=True)  # Ensure password is not returned in the response
    class Meta:
        schema_name = "UserAccount"

class LandBoundarySchema(Schema):
    id = fields.Int(dump_only=True)
    user_id = fields.Int(dump_only=True)
    username = fields.Str(load_only=True)  # Used for input
    boundary = fields.Dict(required=True)  # GeoJSON format expected