from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY="314789074066838946101477291540915153391"
ALGORITHM="HS256"
EXPIRATION_SECONDS_LEFT = 100

def get_pw_hashed(password):
    return pwd_context.hash(password)


def verify_password(plain, hashed):
    return pwd_context.verify(plain, hashed)