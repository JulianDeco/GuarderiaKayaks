import os
import time
from typing import Dict

import jwt
from dotenv import load_dotenv

load_dotenv()


JWT_SECRET = os.getenv("secret")
JWT_ALGORITHM = os.getenv("algorithm")


def token_response(token: str):
    return {
        "access_token": token,
        "token_type": "bearer"
    }

def signJWT(user_id: str, rol: str) -> Dict[str, str]:
    payload = {
        "user_id": user_id,
        "exp": time.time() + 600,
        "rol": rol,
    }
    token = jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)
    print(token)
    return token_response(token)

def decodeJWT(token: str) -> dict:
    decoded_token = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
    return decoded_token if decoded_token["exp"] >= time.time() else None