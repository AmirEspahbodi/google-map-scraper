from typing import Annotated
from fastapi import Depends, Request
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from database import User
from core.connection.database import connection
from core.exception import (
    AuthenticationFailedException,
    AuthenticationRequiredException,
    ConnectionException,
)
from core.security import JWTHandler


class AuthenticationRequired:
    @staticmethod
    async def check_auth(
        req: Request,
        db: Annotated[AsyncSession, Depends(connection)],
        credentials: Annotated[
            HTTPAuthorizationCredentials, Depends(HTTPBearer(auto_error=False))
        ],
    ):
        if not credentials:
            raise AuthenticationRequiredException()
        token = credentials.credentials

        if token is None:
            raise AuthenticationRequiredException()

        payload = JWTHandler.decode(token)
        user_id = payload.get("user_id")

        try:
            user = (
                (
                    await db.execute(
                        select(User)
                        .where(User.id == user_id)
                        .where(User.is_deleted == False)
                    )
                )
                .scalars()
                .first()
            )
        except BaseException as e:
            raise ConnectionException()

        if user is None:
            raise AuthenticationFailedException()

        return user
