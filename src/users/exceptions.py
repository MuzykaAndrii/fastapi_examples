from fastapi import HTTPException


class JwtNotValidError(Exception):
    pass


class JWTExpiredError(Exception):
    pass


class UserError(Exception):
    pass


class UserUnauthenticatedError(HTTPException, UserError):
    def __init__(self) -> None:
        super(HTTPException, self).__init__(status_code=401, detail="Unauthenticated")


class UserLoginError(UserError):
    pass


class UserNotFoundError(UserLoginError):
    pass


class UserInvalidPassword(UserLoginError):
    pass


class UserRegisterError(UserError):
    pass


class EmailAlreadyInUseError(UserRegisterError):
    pass


class UsernameAlreadyInUseError(UserRegisterError):
    pass
