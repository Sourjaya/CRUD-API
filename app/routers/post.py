from .. import models , schemas , utils , oauth2
from fastapi import FastAPI, Response, status, HTTPException,Depends, APIRouter
from sqlalchemy.orm import Session
from ..database import get_db
from typing import List, Optional
from sqlalchemy import func

router=APIRouter(prefix="/posts", tags=['Posts'])
#get all posts
@router.get("/",response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user:int= Depends(oauth2.get_current_user), limit:int=10,skip:int=0,search:Optional[str]=""):

    #sql_query
    #cursor.execute("""SELECT * FROM posts""")
    #posts=cursor.fetchall()
    #print(posts)
    #posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    posts=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote, isouter=True).group_by(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts
#create a post
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)#change default status code
def create_posts(post:schemas.PostCreate,db: Session = Depends(get_db), current_user:int= Depends(oauth2.get_current_user)):
    #to convert pydante model to dict
    #print(post.dict())
    
    #post_dict =post.dict()
    #post_dict['id']=randrange(0,1000000)
    #my_posts.append(post_dict)

    #sql_query
    # cursor.execute("""INSERT INTO posts (title, content, published, rating) VALUES (%s, %s, %s, %s) RETURNING * """, (post.title, post.content, post.published, post.rating))
    # new_post = cursor.fetchone()
    # conn.commit()
    # new_post=models.Post(title=post.title, content=post.content, published=post.published, rating=post.rating)
    print(current_user)
    if current_user == None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not logged in")
    new_post=models.Post(owner_id=current_user.id, **post.dict())#unpacking the dict using ** so that we dont have to write each key value pair
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    print(current_user.email)
    return new_post

#get a particular post
@router.get("/{id}",response_model=schemas.PostOut)
def get_post(id:int,response: Response,db: Session = Depends(get_db), current_user:int= Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id=%s""", (str(id),))
    # post=cursor.fetchone()

    #post=db.query(models.Post).filter(models.Post.id==id).first()
    post=db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote, isouter=True).group_by(models.Post).filter(models.Post.id==id).first()
    
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id: {id} was not found')
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {'message':f'post with id: {id} was not found'}
    return post

#delete a particular post
@router.delete("/{id}" , status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db: Session = Depends(get_db), current_user:int= Depends(oauth2.get_current_user)):
    #deleting post
    #find the index in the array that has the id
    # cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING * """, (str(id),))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    deleted_post=db.query(models.Post).filter(models.Post.id==id)

    if deleted_post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id:{id} does not exist')
    
    if deleted_post.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f'You are not the owner of the post with id:{id}')
    deleted_post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

#update a particular post
@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int,updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user:int= Depends(oauth2.get_current_user)):

    # cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s, rating=%s WHERE id=%s RETURNING * """, (post.title, post.content, post.published, post.rating, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()

    post_query=db.query(models.Post).filter(models.Post.id==id)
    post=post_query.first()

    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'post with id:{id} does not exist')

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f'You are not the owner of the post with id:{id}')
    

    #post_dict =post.dict()
    #post_dict['id']=id
    #my_posts[index]=post_dict
    post_query.update(updated_post.dict(),synchronize_session=False)
    db.commit()
    return post_query.first()