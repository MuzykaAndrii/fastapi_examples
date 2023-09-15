class UserError(Exception):
    pass


class UserNotFoundError(UserError):
    pass


class UserInvalidPassword(UserError):
    pass


class UserCredentialsError(UserError):
    pass


class EmailAlreadyInUseError(UserCredentialsError):
    pass


class UsernameAlreadyInUseError(UserCredentialsError):
    pass
