from dotenv import load_dotenv; load_dotenv()
import os
import jwt

JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")

if JWT_SECRET_KEY is not None:
    print("Below is API Key:")
    print(jwt.encode({}, JWT_SECRET_KEY, algorithm='HS256'))
else:
    print("JWT_SECRET_KEY in the .env file is not properly set up!")