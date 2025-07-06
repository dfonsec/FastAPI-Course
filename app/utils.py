import bcrypt
bcrypt.__about__ = bcrypt
from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Telling passlib to use the bcrypt algorithm to encrypt passwords
def hash(password: str):
    return pwd_context.hash(password)