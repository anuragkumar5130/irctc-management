import os

class Config:
    SECRET_KEY = 'your_secret_key'
    SQLALCHEMY_DATABASE_URI = 'postgresql://neondb_owner:npg_NXOTZjzD8i4k@ep-restless-voice-a8b6t02o-pooler.eastus2.azure.neon.tech/neondb?sslmode=require'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    ADMIN_API_KEY = "admin"
