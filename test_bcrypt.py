from passlib.context import CryptContext

pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

hashed = pwd_context.hash("hello123")
print(hashed)

print(pwd_context.verify("hello123", hashed))