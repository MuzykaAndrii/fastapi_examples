from starlette_admin.contrib.sqla import ModelView

from users.models import Role, User


class UserAdminView(ModelView):
    def __init__(self, *args, **kwargs):
        model = User
        icon = "fa-regular fa-user"
        name = "Users"
        label = None
        identity = None
        converter = None

        super().__init__(model, icon, name, label, identity, converter)

    exclude_fields_from_list = ["hashed_password"]
    exclude_fields_from_detail = ["hashed_password"]
    exclude_fields_from_edit = ["hashed_password"]


class RoleAdminView(ModelView):
    def __init__(self, *args, **kwargs):
        model = Role
        icon = "fa-user-tie"
        name = "Roles"
        label = None
        identity = None
        converter = None

        super().__init__(model, icon, name, label, identity, converter)
