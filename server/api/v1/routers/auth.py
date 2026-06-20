from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from api.dependencies import get_user_service
from api.v1.schemas.token import Token
from api.v1.schemas.user import RegisterRequest, UserResponse
from application.exceptions import InvalidAdminKeyError, InvalidCredentialsError, UserAlreadyExistsError, UsernameCannotBeEmpty
from application.services.user_service import UserService

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/token", response_model=Token)
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    service: UserService = Depends(get_user_service),
) -> Token:
    try:
        token = service.login(form.username, form.password)
    except InvalidCredentialsError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return Token(access_token=token)


@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(
    body: RegisterRequest,
    service: UserService = Depends(get_user_service),
) -> UserResponse:
    try:
        user = service.register(body.username, body.password, body.role, body.admin_key)
    except InvalidAdminKeyError:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Invalid admin registration key")
    except UserAlreadyExistsError as exc:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(exc))
    except UsernameCannotBeEmpty:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Username cannot be empty")
    return UserResponse.from_entity(user)
