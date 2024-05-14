from dotenv import load_dotenv; load_dotenv()
from utils import makeNewJWTSecret
import os
import jwt

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")

if JWT_SECRET_KEY is None:
    makeNewJWTSecret()
    load_dotenv()
    load_dotenv()
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")

print("Below is API Key:")
print(jwt.encode({}, JWT_SECRET_KEY, algorithm='HS256'))