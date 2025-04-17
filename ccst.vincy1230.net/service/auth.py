from fastapi import Header, HTTPException
import os

TOKEN = os.getenv("TOKEN")


def verify_token(authorization: str = Header(...)) -> None:
    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401, detail="Invalid authorization header format"
        )

    token = authorization.split("Bearer ")[1].strip()
    if token != TOKEN:
        raise HTTPException(status_code=403, detail=f"Invalid token")
