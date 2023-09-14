class UserError(Exception):
    pass


class UserCredentialsError(UserError):
    pass


class EmailAlreadyInUseError(UserCredentialsError):
    pass


class UsernameAlreadyInUseError(UserCredentialsError):
    pass
