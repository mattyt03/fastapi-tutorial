from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import models, schemas, utils, oauth2
from ..database import get_db
from sqlalchemy.orm import Session


router = APIRouter(tags=['Authentication'])


@router.post('/login', response_model=schemas.Token)
# learn about dependency functions!!
# OAuth2PasswordRequestForm expects the user's credentials as form data, not raw json
def login(credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == credentials.username).first()
    if user == None:
        # we don't want to specify whether the username or password is incorrect
        # we should simply return 'invalid credentials'
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Invalid Credentials')
    if not utils.verify_password(credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'Invalid Credentials')
    # what else could you put in the payload?
    access_token = oauth2.create_access_token(data = {'user_id': user.id})
    # what is a bearer token?
    return {'access_token': access_token, 'token_type': 'bearer'}