from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware

from auth.models import User
from auth.initialization import auth_backend, fastapi_users, current_user
from auth.schemas import UserRead, UserCreate
from operations.router import router as router_operation


app = FastAPI(
    title="Learning app",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['http://localhost:8000'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth/jwt",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth/jwt",
    tags=["Auth"],
)

app.include_router(router_operation)


@app.get("/protected-route")
def protected_route(user: User = Depends(current_user)):
    return f"Hello, {user.username}"