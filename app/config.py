import os
from dotenv import load_dotenv

load_dotenv()  # loads .env variables

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY")
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    MYSQL_HOST = os.getenv("MYSQL_HOST")       # localhost
    MYSQL_USER = os.getenv("MYSQL_USER")       # root
    MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")  # empty
    MYSQL_DB = os.getenv("MYSQL_DB")           # finance