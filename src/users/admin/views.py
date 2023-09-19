from starlette_admin.contrib.sqla.ext.pydantic import ModelView
from users.admin.schemas import RoleAdminSchema, UserAdminSchema

from users.models import Role, User


class UserAdminView(ModelView):
    def __init__(self, *args, **kwargs):
        model = User
        pydantic_model = UserAdminSchema
        icon = "fa-regular fa-user"
        name = "Users"
        label = None
        identity = None

        super().__init__(model, pydantic_model, icon, name, label, identity)

    exclude_fields_from_list = ["hashed_password"]
    exclude_fields_from_detail = ["hashed_password"]
    exclude_fields_from_edit = ["hashed_password"]


class RoleAdminView(ModelView):
    def __init__(self, *args, **kwargs):
        model = Role
        pydantic_model = RoleAdminSchema
        icon = "fa-user-tie"
        name = "Roles"
        label = None
        identity = None

        super().__init__(model, pydantic_model, icon, name, label, identity)
