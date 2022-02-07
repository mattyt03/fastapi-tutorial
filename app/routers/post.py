from fastapi import APIRouter, Response, status, HTTPException, Depends
from typing import List, Optional
from .. import models, schemas, oauth2
# use two dots to go up a directory
from ..database import get_db
from sqlalchemy.orm import Session


# router objects allow the fastapi app to access path operations from different files
# all path operations in this router will start with /posts
# the tag is used to categorize path operations in the documentation
router = APIRouter(prefix='/posts', tags=['Posts'])


# in each path operation, the database gets passed in as a parameter
# it's a session object that gets created using the get_db dependency

# for retrieving posts, the user doesn't have to be logged in. Hence there is no oauth2 dependency included in those path operations
# for creating, updating, and deleting posts, the user should definitely be logged in


@router.get('/', response_model=List[schemas.PostResponse])
# fastapi will look for query/path parameters with the same name as the parameters in the function below
# to encode spaces in a query param, write %20
# Non-default arguments can't follow default arguments
def get_posts(db: Session = Depends(get_db), limit: int = 10, skip: int = 0, search: str = ''):
    # filter is equivalent to the where keyword in sql
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # fastapi will automatically convert posts to the response model that we provided in the decorator, then to json,
    # and send it back as the body of an http response
    return posts


@router.get('/{id}', response_model=schemas.PostResponse)
# id automatically gets converted to an int
def get_post(id: int, db: Session = Depends(get_db)):
    # all() and first() are similar to the fetch() methods
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if post == None:
        # review raise
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} does not exist')
    return post


# status code should be 201 for post requests
@router.post('/', status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
# fastapi will automatically pass the body of the post request into this function
# the body of the post request automatically gets converted to a Post model
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db), user = Depends(oauth2.get_current_user)):
    # this creates a new post object (we're calling a constructor method that was automatically defined)
    ''' new_post = models.Post(title=post.title, content=post.content, published=post.published) '''
    # converting post to a dictionary and unpacking it produces the same format as above but is much simpler/cleaner
    new_post = models.Post(owner_id = user.id, **post.dict())
    # this adds the new post object to the database
    db.add(new_post)
    db.commit()
    # retrieves the new post that we created (similar to RETURNING *) and stores it back into the new_post variable
    db.refresh(new_post)
    return new_post


# status code should be 204 for delete requests
@router.delete('/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), user = Depends(oauth2.get_current_user)):
    # we store the query so we can chain the delete() method to it later
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} does not exist')
    # check if the user who sent the delete request owns this post (they shouldn't be able to delete other people's posts)
    if post.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'not authorized to perform requested action')
    # what is synchronize_session?
    post_query.delete(synchronize_session=False)
    db.commit()
    return {'message': f'post {id} was successfully deleted'}


@router.put('/{id}', response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), user = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} does not exist')
    if post.owner_id != user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'not authorized to perform requested action')
    # the update() method takes a dictionary with the updated entry as a parameter
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()