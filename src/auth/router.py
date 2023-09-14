from fastapi import APIRouter


router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)


@router.post("/register")
async def register_user():
    ...


@router.post("/login")
async def login_user():
    ...


@router.post("/logout")
async def logout_user():
    ...
