from flask.views import MethodView
from flask_smorest import Blueprint
from flask import request, jsonify, render_template
import requests
from dotenv import load_dotenv
import os

load_dotenv()

YOUTUBE_API_KEY = os.getenv('YOUTUBE_API_KEY')

youtube_bp = Blueprint('youtube', __name__, url_prefix='/youtube', description="Operations on YouTube videos")

class YouTubeVideos(MethodView):
    
    def get(self):
        """Fetch YouTube videos based on the query and return HTML or JSON response"""
        query = request.args.get('query', "deforestation dangers")  # Default query if none is provided
        
        # URL for YouTube API search
        url = f"https://www.googleapis.com/youtube/v3/search?part=snippet&maxResults=5&q={query}&type=video&key={YOUTUBE_API_KEY}"

        response = requests.get(url)
        
        # If the API call is successful
        if response.status_code == 200:
            data = response.json()
            videos = [
                {
                    "title": item['snippet']['title'],
                    "video_id": item['id']['videoId'],
                    "description": item['snippet']['description']
                }
                for item in data['items']
            ]
            
            # Return HTML response
            if request.accept_mimetypes.best_match(['application/json', 'text/html']) == 'text/html':
                return render_template('youtube.html', videos=videos)
            
            # Return JSON response
            return jsonify(videos)
        
        # Handle failure in API request
        return jsonify({"error": "Failed to fetch videos"}), 500


# Add the class-based view to the blueprint
youtube_bp.add_url_rule("/youtube-videos", view_func=YouTubeVideos.as_view("youtube_videos"))

