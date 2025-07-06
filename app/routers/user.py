from ..schemas import UserOut, UserCreate
from ..models import User
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import status, HTTPException, Depends, APIRouter


router = APIRouter()

@router.post("/users", status_code=status.HTTP_201_CREATED, response_model=UserOut)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    # cursor.execute("""INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING *""", 
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    
    
    # Hash the password - user.password
    hashed_password = hash(user.password)
    user.password = hashed_password
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    
    # refresh takes the entry that was created in the db and updates the python object data to reflect what's in the db
    db.refresh(new_user)
    
    return new_user
    
@router.get("/users/{id}", response_model=UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'User with id: {id} does not exist')
    
    
    return user
    