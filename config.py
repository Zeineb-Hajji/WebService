class Config:
    # Database URI, use an appropriate URI for your setup
    SQLALCHEMY_DATABASE_URI = 'sqlite:///site.db'  # For SQLite, or change it for another DB like PostgreSQL or MySQL
    SQLALCHEMY_TRACK_MODIFICATIONS = False  # Disable modification tracking for performance reasons
    SECRET_KEY = '1210'  # Change this to a more secure key for production

    # You can add other configuration variables here as needed
    # For example, you might want to add email configuration or API keys
