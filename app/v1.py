from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange


app = FastAPI()

# learn more ab pydantic models
# the body of a post request will be parsed using the template below
# the name and type of each field must match exactly
class Post(BaseModel):
    title: str
    content: str
    # published field is optional, defaults to true
    published: bool = True


posts = [{'title': 'title of post 1', 'content': 'content of post 1', 'published': True, 'id': 1},
         {'title': 'title of post 2', 'content': 'content of post 2', 'published': True, 'id': 2}]


# learn more ab decorators
# when a get requests is sent to this url, the function associated with the decorator gets executed
@app.get("/")
async def root():
    return {'message": "welcome to my api'}


@app.get('/posts')
def get_posts():
    # learn more ab how this works
    # fastapi will automatically convert posts to json and send it back as an http response
    return {'data': posts}


@app.get('/posts/{id}')
# fastapi knows that the id paramter should be the value of the id path variable
# id automatically gets converted to an int
def get_post(id: int):
    post = [post for post in posts if post['id'] == id]
    if len(post) == 0:
        # review raise
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} does not exist')
    return {'data': post[0]}


# status code should be 201 for post requests
@app.post('/posts', status_code=status.HTTP_201_CREATED)
# fastapi will automatically pass the body of the post request into this function
# the body of the post request automatically gets converted to a Post model
def create_post(post: Post):
    post_dict = post.dict()
    # this is not a good idea for production
    post_dict['id'] = randrange(0, 1000000)
    posts.append(post_dict)
    return {'data': post_dict}


def find_index_of_post(id):
    # review enumerate
    for i, p in enumerate(posts):
        if p['id'] == id:
            return i


# status code should be 204 for delete requests
@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # posts[:] = [post for post in posts if post['id'] != id]
    index = find_index_of_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} does not exist')
    posts.pop(index)
    return {'message': f'post {id} was successfully deleted'}


@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    index = find_index_of_post(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} does not exist')
    post_dict = post.dict()
    post_dict['id'] = id
    posts[index] = post_dict
    return {'data': post_dict}