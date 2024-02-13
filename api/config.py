import os
from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    PROJECT_NAME: str = "Kly.lol API"
    DESCRIPTION: str = (
        "Kly.lol is a URL shortener service powered by Gemini with FastAPI and Next.js."
    )
    VERSION: str = "0.2.0"
    DATABASE_URI: str = (
        f"postgresql://{os.environ['DATABASE_USERNAME']}:{os.environ['DATABASE_PASSWORD']}@{os.environ['DATABASE_HOST']}/{os.environ['DATABASE_NAME']}?sslmode=require"
    )

    CLERK_BACKEND_API_URL: str = os.environ["CLERK_BACKEND_API_URL"]
    CLERK_FRONTEND_API_URL: str = os.environ["CLERK_FRONTEND_API_URL"]
    CLERK_SECRET_KEY: str = os.environ["CLERK_SECRET_KEY"]
    CLERK_JWKS_URL: str = os.environ["CLERK_JWKS_URL"]
    NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY: str = os.environ[
        "NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY"
    ]
    access_token_expire_minutes: str = os.environ.get(
        "ACCESS_TOKEN_EXPIRE_MINUTES", "5"
    )
    refresh_token_expire_minutes: str = os.environ.get(
        "REFRESH_TOKEN_EXPIRE_MINUTES", "10"
    )
    secret_key: str = os.environ.get("SECRET_KEY", "VT3BlbkFJmqaji32ruwrd43jmhb3s")
    algorithm: str = os.environ.get("ALGORITHM", "HS256")

    class ConfigDict:
        env_file = ".env"


settings = Settings()
