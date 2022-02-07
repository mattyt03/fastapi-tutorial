from jose import jwt, JWTError
from datetime import datetime, timedelta
from . import schemas, models
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer
from .database import get_db
from sqlalchemy.orm import Session
from .config import settings


# the tokenURL parameter doesn't create that path operation, but declares that the URL /login will be the one that the client should use to get the token
# that information is used in OpenAPI, and then in the interactive API documentation systems
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')


# the contents of the data dictionary will be put in the payload of the token
def create_access_token(data: dict):
    to_encode = data.copy()
    # add the expiration time to the payload
    expiration_time = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)
    # the field name MUST be exp!!
    to_encode.update({'exp': expiration_time})
    # create the token
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, algorithm=settings.algorithm)
    return encoded_jwt


# # does the exception really need to be a parameter?
# def verify_access_token(token: str, credentials_exception):
#     try:
#         # the decode() method verifies that the token is valid and returns the payload as a dictionary
#         payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
#         # use .get() to extract a specific field from the payload
#         id: str = payload.get('user_id')
#         # isn't this a bit redundant?
#         if id is None:
#             raise credentials_exception
#         # do we really need a pydantic model for this?
#         token_data = schemas.TokenData(id=id)
#     # learn more ab this error
#     except JWTError:
#         raise credentials_exception

#     return token_data


def verify_access_token(token: str):
    try:
        # the decode() method verifies that the token is valid and returns the payload as a dictionary
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
    # learn more ab this error
    except JWTError:
        # what is the WWW-Authenticate header for?
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
                            detail=f'Invalid Credentials', headers={'WWW-Authenticate': 'Bearer'})
    return payload


# # Depends(oauth2_scheme) will check if an api request includes an Authorization header with the value Bearer plus an access token
# # this is the format for the password "flow" defined in OAuth2
# def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
#     # what is the WWW-Authenticate header for?
#     credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED,
#                                           detail=f'Invalid Credentials', headers={'WWW-Authenticate': 'Bearer'})   
#     token_data = verify_access_token(token, credentials_exception)
#     user = db.query(models.User).filter(models.User.id == token_data.id).first()
#     # user is an orm model not a pydantic model
#     return user


# Depends(oauth2_scheme) will check if an api request includes an Authorization header with the value Bearer plus an access token
# this is the format for the password "flow" defined in OAuth2
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    token_payload = verify_access_token(token)
    user = db.query(models.User).filter(models.User.id == token_payload['user_id']).first()
    # remember user is an orm model not a pydantic model
    return user