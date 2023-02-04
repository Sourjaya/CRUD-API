
from fastapi import FastAPI, Response, HTTPException,Depends
#from fastapi.params import Body
from . import models
from .database import engine
from .routers import user, post , auth ,vote
from .config import settings
from fastapi.middleware.cors import CORSMiddleware
#models.Base.metadata.create_all(bind=engine)

app=FastAPI()
origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
# my_posts = []

# def find_post(id):
#     for p in my_posts:
#         if p['id']==id:
#             return p

# def find_index_post(id):
#     for i,p in enumerate(my_posts):
#         if p['id'] == id:
#             return i

# @app.get("/sqlalchemy")
# def test_posts(db: Session = Depends(get_db)):
#     posts=db.query(models.Post).all()
#     return {"data":posts}
@app.get("/")
def home():
    return {"message":"Welcome to the home page"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

