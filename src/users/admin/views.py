from fastapi import Request
from starlette_admin import ExportType
from starlette_admin.fields import StringField, DateTimeField

from src.admin.admin import MyModelView
from src.auth.auth import PWDManager
from src.users.admin.schemas import RoleAdminSchema, UserAdminSchema
from src.users.models import Role, User


class UserAdminView(MyModelView):
    def __init__(self, *args, **kwargs):
        model = User
        pydantic_model = UserAdminSchema
        icon = "fa-regular fa-user"
        name = "User"
        label = "Users"
        identity = None

        super().__init__(model, pydantic_model, icon, name, label, identity)

    fields = [
        User.id,
        User.username,
        User.email,
        StringField(
            "password",
            label="Password",
            exclude_from_detail=True,
            exclude_from_edit=True,
            exclude_from_list=True,
        ),
        StringField(
            "hashed_password",
            exclude_from_detail=True,
            exclude_from_edit=True,
            exclude_from_list=True,
            disabled=True,
            input_type="hidden",
            label="",
        ),
        DateTimeField(
            "registered_at",
            exclude_from_create=True,
            exclude_from_edit=True,
        ),
        User.is_active,
        User.is_verified,
        User.is_superuser,
        User.role,
    ]

    export_fields = [
        "id",
        "username",
        "email",
        "registered_at",
    ]
    export_types = [
        ExportType.EXCEL,
        ExportType.PDF,
        ExportType.PRINT,
    ]

    column_visibility = True
    search_builder = True
    responsive_table = True
    save_state = True

    def on_before_create(self, request: Request, data: dict) -> dict:
        raw_password = data.get("password")
        hashed_password = PWDManager.get_password_hash(raw_password)

        data.update({"hashed_password": hashed_password})
        data.pop("password", None)

        return data


class RoleAdminView(MyModelView):
    def __init__(self, *args, **kwargs):
        model = Role
        pydantic_model = RoleAdminSchema
        icon = "fa-user-tie"
        name = "Role"
        label = "Roles"
        identity = None

        super().__init__(model, pydantic_model, icon, name, label, identity)
