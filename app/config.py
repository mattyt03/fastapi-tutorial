from pydantic import BaseSettings

# we use a pydantic model to validate & perform type casting on all our env variables (all env variables are read as a string)
# pydantic will automatically check our system for env variables with the same name as the attributes in this model (case insensitive)
class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_username: str
    database_password: str
    database_name: str
    secret_key: str
    algorithm: str
    access_token_expire_minutes: int

    # tells pydantic to import variables from an env file
    class Config:
        env_file = ".env"

settings = Settings()