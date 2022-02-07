from fastapi import FastAPI
# why do we need the from . ?
# from . import models
from .database import engine
from .routers import post, user, auth
from .config import settings
from fastapi.middleware.cors import CORSMiddleware

# no need to call this command now that we are using alembic
# models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# CORS configuration. For more information visit https://fastapi.tiangolo.com/tutorial/cors/#use-corsmiddleware 
app.add_middleware(
    CORSMiddleware,
    # the list of origins that are allowed to communicate with our api
    # if you want a public api that all domains/origins can access, use "*" (a wildcard)
    allow_origins=["*"],
    allow_credentials=True,
    # we can also restrict access to specific http methods and headers
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)

# learn more ab decorators
# when a get requests is sent to this url, the function associated with the decorator gets executed
@app.get("/")
async def root():
    return {'message': 'Hello World'}