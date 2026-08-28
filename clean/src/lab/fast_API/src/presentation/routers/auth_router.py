from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from lab.fast_API.src.application.dtos import LoginDTO, RegisterUserDTO
from lab.fast_API.src.application.use_cases.register_login_user import (
    LoginUseCase,
    RegisterUserUseCase,
)
from lab.fast_API.src.presentation.dependencies import (
    get_login_use_case,
    get_register_user_use_case,
)
from lab.fast_API.src.presentation.presenters.user_presenter import (
    TokenPresenter,
    UserPresenter,
)
from lab.fast_API.src.presentation.schemas import TokenOut, UserCreateRequest, UserOut

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/register", response_model=UserOut)
def registrar_usuario(
    request: UserCreateRequest,
    use_case: RegisterUserUseCase = Depends(get_register_user_use_case),
):
    dto = RegisterUserDTO(
        username=request.username, 
        email=request.email, 
        password=request.password)
    resultado = use_case.ejecutar(dto)
    return UserPresenter.present(resultado)


@router.post("/login", response_model=TokenOut)
def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    use_case: LoginUseCase = Depends(get_login_use_case),
):
    dto = LoginDTO(username=form_data.username, password=form_data.password)
    resultado = use_case.ejecutar(dto)
    return TokenPresenter.present(resultado)
