from urllib.parse import urlencode
from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import RedirectResponse
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.services.keycloak_client import KeycloakClient
from app.users.schemas import AddTask, AddTaskWithUserId, AddUser, SUserId
from app.config import settings
from app.users.dao import UserDAO
from app.tasks.dao import TasksDAO
from app.services.auth_dep import get_current_user, get_keycloak_client
from app.dao.session_maker import SessionDep, TransactionSessionDep

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/login/callback", include_in_schema=False)
async def login_callback(code: str | None = None,
                         error: str | None = None,
                         error_description: str | None = None,
                         session: AsyncSession = Depends(TransactionSessionDep),
                         keycloak: KeycloakClient = Depends(get_keycloak_client),
                         ) -> RedirectResponse:
    """"Обрабатывает callback после авторизации в Keycloak.
    Получает токен, информацию о пользователе, сохраняет пользователя в бд (если нужно)
    и устанавливает cookie с токенами. Обрабатывает ошибки в Keycloak."""
    if error:
        logger.error(f"Keycloak error: {error}, description: {error_description}")
        raise HTTPException(status_code=401, detail="Authorization code is required")

    if not code:
        raise HTTPException(status_code=401, detail="Authorization code is required")

    try:
        # Получение токенов от Keycloak
        token_data = await keycloak.get_tokens(code)
        print(token_data)
        access_token = token_data.get("access_token")
        refresh_token = token_data.get("refresh_token")
        id_token = token_data.get("id_token")
        if not access_token:
            raise HTTPException(status_code=401, detail="Токен доступа не найден")
        if not refresh_token:
            raise HTTPException(status_code=401, detail="Refresh token не найден")
        if not id_token:
            raise HTTPException(status_code=401, detail="ID token не найден")

        user_info = await keycloak.get_user_info(access_token)
        user_id = user_info.get("sub")
        if not user_id:
            raise HTTPException(status_code=401, detail="ID пользователя не найден")

        # Проверка существования пользователя, создание нового при необходимости
        users_dao = UserDAO(session)
        user = await users_dao.find_one_or_none_by_id(user_id)
        if not user and isinstance(user_info, dict):
            user_info["id"] = user_info.pop("sub")
            await users_dao.add(AddUser(**user_info))

        # Установка cookie с токенами и редирект
        response = RedirectResponse(url="/protected")
        response.set_cookie(
            key="access_token",
            value=access_token,
            httponly=True,
            secure=True,
            samesite="lax",
            path="/",
            max_age=token_data.get("expires_in", 3600),
        )
        response.set_cookie(
            key="refresh_token",
            value=refresh_token,
            httponly=True,
            secure=True,
            samesite="lax",
            path="/",
            max_age=token_data.get("expires_in", 3600),
        )
        response.set_cookie(
            key="id_token",
            value=id_token,
            httponly=True,
            secure=True,
            samesite="lax",
            path="/",
            max_age=token_data.get("expires_in", 3600),
        )
        logger.info(f"User {user_id} logged in successfully")
        return response
    except Exception as e:
        logger.error(f"Ошибка обработки callback'а логина: {str(e)}")
        raise HTTPException(status_code=401, detail="Ошибка авторизации")

