from sqladmin import ModelView

from auth.models import Role, User


class UserAdmin(ModelView, model=User):
    name = "User"
    name_plural = "Users"
    icon = "fa-solid fa-user"

    column_exclude_list = [User.hashed_password]
    column_details_exclude_list = [User.hashed_password]
    form_excluded_columns = [User.hashed_password]


class RoleAdmin(ModelView, model=Role):
    name = "Role"
    name_plural = "Roles"

    column_list = ['id', 'name', 'permissions']