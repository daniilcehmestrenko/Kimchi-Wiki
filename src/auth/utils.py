from .exceptions import UserPasswordDoesNotMatch
from .models import User


async def match_password(user: User, password: str):
    if user.password != password:
        raise UserPasswordDoesNotMatch
