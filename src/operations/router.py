from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError

from database import get_async_session
from operations.models import operation
from operations.schemas import OperationCreate, OperationRead


router = APIRouter(
    prefix="/operations",
    tags=["Operation"],
)


@router.get("/")
async def get_specific_operations(operation_type: str, session: AsyncSession = Depends(get_async_session)) -> list[OperationRead]:
    query = select(operation).where(operation.c.type == operation_type)
    result = await session.execute(query)
    return result.all()


@router.post("/")
async def add_specific_operation(
    new_operation: OperationCreate,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        q = insert(operation).values(new_operation.model_dump())

        res = await session.execute(q)
        await session.commit()

    except IntegrityError:
        raise HTTPException(400, detail={
            "status": "failed",
            "data": None,
            "detail": "Object already exists",
        })
    except Exception:
        raise HTTPException(500, detail={
            "status": "failed",
            "data": None,
            "detail": "Internal server error, contact support",
        })
    else:
        # inserted_id = res.inserted_primary_key[0]
        # created_operation_q = select(operation).where(operation.c.id == inserted_id)
        # created_operation = await session.execute(created_operation_q)

        return {
            "status": "success",
            # "data": OperationRead(**created_operation.all()),
            "data": None,
            "detail": None,
        }


    