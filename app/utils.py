from passlib.context import CryptContext

# here we're telling passlib what hashing algorithm we want to use (bcrypt)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# hashes the password
def hash(password: str):
    return pwd_context.hash(password)

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
