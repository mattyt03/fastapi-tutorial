from fastapi import FastAPI, Response, status, HTTPException
from pydantic import BaseModel
import psycopg2
from psycopg2.extras import RealDictCursor
import time


app = FastAPI()


# the body of a post request will be parsed using the template below
# the name and type of each field must match exactly
class Post(BaseModel):
    title: str
    content: str
    # published field is optional, defaults to true
    published: bool = True


while True:
    # review try & except
    try:
        # last argument in connect() is for including column names
        conn = psycopg2.connect(host='localhost', database='FastAPI',
                                user='postgres', password='maxmat2007', cursor_factory=RealDictCursor)
        # a cursor is a mechanism that enables traversal over the records in a database, akin to an iterator
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    # learn more ab exceptions
    except Exception as error:
        print("Failed to connect to database")
        print("Error: ", error)
        # wait two seconds before trying to connect again
        time.sleep(2) 


# learn more ab decorators
# when a get requests is sent to this url, the function associated with the decorator gets executed
@app.get("/")
async def root():
    return {'message": "welcome to my api'}


@app.get('/posts')
def get_posts():
    # the execute() method executes a database operation (query or command)
    # the method returns None. If a query was executed, the returned values can be retrieved using fetch() methods
    cursor.execute("""SELECT * FROM posts""")
    # why don't they combine the execute and fetch methods?
    # fetchall() returns the rows of a query result as a list of tuples
    posts = cursor.fetchall()
    # fastapi will automatically convert posts to json and send it back as an http response
    return {'data': posts}


@app.get('/posts/{id}')
# fastapi knows that the id paramter should be the value of the id path variable
# id automatically gets converted to an int
def get_post(id: int):
    # the %s value must be a string
    # but we still need to convert id to an int so it can be validated
    cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id)))
    post = cursor.fetchone()
    if post == None:
        # review raise
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} does not exist')
    return {'data': post}


# status code should be 201 for post requests
@app.post('/posts', status_code=status.HTTP_201_CREATED)
# fastapi will automatically pass the body of the post request into this function
# the body of the post request automatically gets converted to a Post model
def create_post(post: Post):
    # use %s instead of formatted strings to avoid SQL injection attacks
    cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", (post.title,
                   post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {'data': new_post}


# status code should be 204 for delete requests
@app.delete('/posts/{id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute(
        """DELETE FROM posts WHERE id = %s RETURNING *""", (str(id)))
    deleted_post = cursor.fetchone()
    conn.commit()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} does not exist')
    return {'message': f'post {id} was successfully deleted'}


@app.put('/posts/{id}')
def update_post(id: int, post: Post):
    cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",
                   (post.title, post.content, post.published, str(id)))
    updated_post = cursor.fetchone()
    conn.commit()
    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f'post with id {id} does not exist')
    return {'data': updated_post}