from pydantic import BaseSettings

class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_name: str
    database_username: str
    database_password: str
    jwt_secret_key: str
    jwt_algorithm: str
    jwt_expiration_time: int

    class Config:
        env_file = '.env'

settings = Settings()
