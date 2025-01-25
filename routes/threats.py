from flask_smorest import Blueprint
from flask import request, jsonify
from models import Threat
from schemas import ThreatSchema
from db import db
import io
import matplotlib.pyplot as plt
from flask import send_file


threats_bp = Blueprint('threats', __name__, url_prefix='/api', description='Threats Operations')

@threats_bp.route('/threats', methods=['POST'])
def add_threat():
    data = request.get_json()
    try:
        threat = ThreatSchema().load(data)
        new_threat = Threat(**threat)
        db.session.add(new_threat)
        db.session.commit()
        return jsonify(ThreatSchema().dump(new_threat)), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400
@threats_bp.route('/threats/piechart/<int:region_id>', methods=['GET'])
def get_threat_piechart(region_id):
    try:
        # Query all threats for the given region
        threats = Threat.query.filter_by(region_id=region_id).all()
        if not threats:
            return jsonify({"error": "No threats found for this region"}), 404

        # Define weights
        biodiversity_weights = {"Low": 1, "Medium": 2, "High": 3,"Very High":4}
        soil_weights = {"Mild": 1, "Moderate": 2, "Severe": 3}

        # Initialize weighted values
        total_co2 = sum(threat.co2_emissions for threat in threats)
        total_biodiversity = sum(biodiversity_weights.get(threat.biodiversity_loss, 0) for threat in threats)
        total_soil = sum(soil_weights.get(threat.soil_degradation, 0) for threat in threats)

        # Normalize CO2 emissions (scaling down by max value or constant)
        max_co2 = max(threat.co2_emissions for threat in threats) if threats else 1
        normalized_co2 = sum(threat.co2_emissions / max_co2 for threat in threats)

        # Total weight for normalization
        total_weight = normalized_co2 + total_biodiversity + total_soil
        if total_weight == 0:
            return jsonify({"error": "No valid data to generate the chart"}), 404

        # Calculate percentages
        percentages = [
            (normalized_co2 / total_weight) * 100,
            (total_biodiversity / total_weight) * 100,
            (total_soil / total_weight) * 100,
        ]

        # Pie chart labels
        labels = ["CO2 Emissions", "Biodiversity Loss", "Soil Degradation"]

        # Generate the pie chart
        fig, ax = plt.subplots()
        wedges, texts, autotexts = ax.pie(
            percentages, labels=labels, autopct='%1.1f%%', startangle=90,
            textprops=dict(color="w")
        )
        ax.axis('equal')  # Equal aspect ratio ensures the pie chart is circular
        # Customize label and percentage font size
        plt.setp(autotexts, size=10, weight="bold")
        plt.setp(texts, size=10)

        plt.title(f"Threat Intensity for Region {region_id}", fontsize=14)

        # Save the plot to an in-memory buffer
        img = io.BytesIO()
        plt.savefig(img, format='png')
        img.seek(0)
        plt.close(fig)  # Close the plot to free memory

        # Return the image as a response
        return send_file(img, mimetype='image/png')
    except Exception as e:
        return jsonify({"error": str(e)}), 500
