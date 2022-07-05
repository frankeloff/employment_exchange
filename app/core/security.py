from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext

myctx = CryptContext(schemes=["sha256_crypt", "md5_crypt"])


def hash_password(password: str) -> str:
    return myctx.hash(password)


def verify_password(password: str, hash: str) -> bool:
    return myctx.verify(password, hash)


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/token")
