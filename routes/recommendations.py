from flask_smorest import Blueprint
from flask import request, jsonify, render_template, Response
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle,Paragraph
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from models import Recommendation, Region
from schemas import RecommendationSchema
from db import db
import io

recommendations_bp = Blueprint('recommendations', __name__, url_prefix='/api', description='Recommendations Operations')

recommendation_schema = RecommendationSchema()
recommendations_schema = RecommendationSchema(many=True)

@recommendations_bp.route('/recommendations', methods=['GET'])
def get_all_recommendations():
    # Fetch all recommendations from the database
    recommendations = Recommendation.query.all()
    recommendation_data = recommendations_schema.dump(recommendations)

    # Prepare the PDF buffer
    pdf_buffer = io.BytesIO()
    doc = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    
    
    styles = getSampleStyleSheet()
    normal_style = styles['Normal']

    # Table header
    table_data = [["Region Name", "Threat Type", "Recommendation"]]

    # Populate table rows
    
    for recommendation in recommendation_data:
        region = Region.query.get(recommendation['region_id'])  # Fetch the region name using the foreign key
        region_name = region.name if region else "Unknown"
        
        table_data.append([
            Paragraph(region_name, normal_style),
            Paragraph(recommendation['threat_type'], normal_style),
            Paragraph(recommendation['recommendation'], normal_style)
            ])
        page_width, _ = letter
        column_widths = [page_width * 0.3, page_width * 0.2, page_width * 0.5]
    # Create the table
    table = Table(table_data,colWidths=column_widths)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Header background color
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Header text color
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),  # Align text to the left
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Header font
        ('FONTSIZE', (0, 0), (-1, 0), 12),  # Header font size
        ('BOTTOMPADDING', (0, 0), (-1, 0), 10),  # Padding for the header
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Row background color
        ('GRID', (0, 0), (-1, -1), 1, colors.black)  # Grid lines
    ]))

    # Add the table to the document
    elements = [table]
    doc.build(elements)

    # Return the PDF as a response
    pdf_buffer.seek(0)
    response = Response(pdf_buffer, content_type='application/pdf')
    response.headers['Content-Disposition'] = 'inline; filename="recommendations.pdf"'
    return response


@recommendations_bp.route('/recommendations/<int:region_id>', methods=['GET'])
def get_recommendations_by_region(region_id):
    recommendations = Recommendation.query.filter_by(region_id=region_id).all()
    if not recommendations:
        return jsonify({"error": "No recommendations found for this region"}), 404
    return jsonify(recommendations_schema.dump(recommendations)), 200

@recommendations_bp.route('/recommendations', methods=['POST'])
def add_recommendation():
    data = request.get_json()
    try:
        # Validate region exists
        region = Region.query.get(data.get('region_id'))
        if not region:
            return jsonify({"error": "Region not found"}), 404

        recommendation = recommendation_schema.load(data)
        new_recommendation = Recommendation(**recommendation)
        db.session.add(new_recommendation)
        db.session.commit()
        return jsonify(recommendation_schema.dump(new_recommendation)), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@recommendations_bp.route('/recommendations/<int:recommendation_id>', methods=['PUT'])
def update_recommendation(recommendation_id):
    recommendation = Recommendation.query.get(recommendation_id)
    if not recommendation:
        return jsonify({"error": "Recommendation not found"}), 404
    
    data = request.get_json()
    try:
        for key, value in data.items():
            setattr(recommendation, key, value)
        db.session.commit()
        return jsonify(recommendation_schema.dump(recommendation)), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@recommendations_bp.route('/recommendations/<int:recommendation_id>', methods=['DELETE'])
def delete_recommendation(recommendation_id):
    recommendation = Recommendation.query.get(recommendation_id)
    if not recommendation:
        return jsonify({"error": "Recommendation not found"}), 404
    
    db.session.delete(recommendation)
    db.session.commit()
    return jsonify({"message": "Recommendation deleted successfully"}), 200
