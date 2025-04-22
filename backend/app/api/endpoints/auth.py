from fastapi import APIRouter, Depends
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import JWTStrategy, AuthenticationBackend, CookieTransport
from app.db.user import User, UserRead, UserCreate
from app.db.user_manager import UserManager, SECRET
from app.db.session import SessionLocal
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.orm import sessionmaker
import sqlalchemy

router = APIRouter()

# Database setup for FastAPI Users
DATABASE_URL = "postgresql+psycopg2://coach:coachpw@db:5432/code_coach"
engine = sqlalchemy.create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
user_db = SQLAlchemyUserDatabase(User, SessionLocal())

# JWT auth backend
cookie_transport = CookieTransport(cookie_name="code_coach_auth", cookie_max_age=3600)

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600)

auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_jwt_strategy,
)

# Provide a dependency function for UserManager
async def get_user_manager(user_db=Depends(lambda: user_db)):
    yield UserManager(user_db)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager=get_user_manager,
    auth_backends=[auth_backend],
)

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserCreate),
    prefix="/users",
    tags=["users"],
)
