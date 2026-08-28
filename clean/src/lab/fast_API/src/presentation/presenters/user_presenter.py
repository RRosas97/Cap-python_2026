from lab.fast_API.src.application.dtos import TokenDTO, UserDTO
from lab.fast_API.src.presentation.schemas import TokenOut, UserOut


class UserPresenter:
    @staticmethod
    def present(dto: UserDTO) -> UserOut:
        return UserOut(id=dto.id, username=dto.username, email=dto.email)


class TokenPresenter:
    @staticmethod
    def present(dto: TokenDTO) -> TokenOut:
        return TokenOut(access_token=dto.access_token, token_type=dto.token_type)
