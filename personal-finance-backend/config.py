class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///expenses.db'  # Replace with your DB URI (e.g., PostgreSQL, MySQL, etc.)
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = 'your-secret-key'  # Replace with a more secure key in production



