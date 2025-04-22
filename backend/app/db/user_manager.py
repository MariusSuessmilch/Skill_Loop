from fastapi_users import BaseUserManager, IntegerIDMixin
from app.db.user import User
from app.db.session import SessionLocal

SECRET = "CHANGE_THIS_SECRET"  # Change this to a secure value in production

class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request=None):
        print(f"User {user.email} has registered.")
