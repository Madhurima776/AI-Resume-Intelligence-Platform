from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

def hash_password(password):
    return pwd_context.hash(str(password))

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(
        str(plain_password),
        hashed_password
    )