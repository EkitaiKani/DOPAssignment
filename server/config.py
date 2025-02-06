import os

class Config:
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class DevelopmentConfig(Config):
    DB_HOST = os.getenv("DB_HOST")
    DB_NAME = os.getenv("DB_NAME")
    DB_USER = os.getenv("DB_USER")
    DB_PASSWORD = os.getenv("DB_PASSWORD")
    SQLALCHEMY_DATABASE_URI = f"postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    
    def __init__(self):
        print(f"Database URI: {self.SQLALCHEMY_DATABASE_URI}")
        print(f"Host: {self.DB_HOST}")
        print(f"User: {self.DB_USER}")
        print(f"Database: {self.DB_NAME}")

class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL")

# ENV = os.getenv("FLASK_ENV", "development")
# if ENV == "production":
#     AppConfig = ProductionConfig
# else:
#     AppConfig = DevelopmentConfig

