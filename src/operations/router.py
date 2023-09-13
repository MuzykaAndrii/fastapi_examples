from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import delete, insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import (
    IntegrityError,
    NoResultFound,
)

from fastapi_cache.decorator import cache

from database import get_async_session
from operations.models import Operation
from operations.schemas import (
    OperationCreate,
    OperationRead,
)


router = APIRouter(
    prefix="/operations",
    tags=["Operation"],
)


@router.get("/{operation_id}/")
async def get_operation(
    operation_id: int,
    session: AsyncSession = Depends(get_async_session),
) -> OperationRead | None:
    return await session.get(Operation, operation_id)


@router.delete("/{operation_id}/")
async def delete_operation(
    operation_id: int,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        stmt = (
            delete(Operation).where(Operation.id == operation_id).returning(Operation)
        )
        result = await session.execute(stmt)

        await session.commit()
    except NoResultFound:
        raise HTTPException(
            404,
            detail={
                "status": "failed",
                "data": None,
                "detail": "Record not found",
            },
        )
    except Exception:
        raise HTTPException(
            500,
            detail={
                "result": "failed",
                "data": None,
                "detail": "Internal error",
            },
        )
    else:
        return {
            "status": "success",
            "data": result.scalar_one(),
            "detail": "Record successfully deleted",
        }


@router.get("/", response_model=list[OperationRead])
@cache(expire=60)
async def get_operations_by_type(
    operation_type: str,
    session: AsyncSession = Depends(get_async_session),
) -> list[OperationRead]:
    query = select(Operation).where(Operation.type == operation_type)
    result = await session.execute(query)
    return result.scalars().all()


@router.post("/", status_code=201)
async def add_operation(
    new_operation: OperationCreate,
    session: AsyncSession = Depends(get_async_session),
):
    try:
        # stmt = insert(Operation).values(new_operation.model_dump())

        # res = await session.execute(stmt)
        # print(res.inserted_primary_key)
        # await session.commit()

        operation = Operation(**new_operation.model_dump())
        session.add(operation)
        await session.commit()

        # refresh obj to get actual data (useful if on db-side received data changes)
        await session.refresh(operation)

    except IntegrityError:
        raise HTTPException(
            400,
            detail={
                "status": "failed",
                "data": None,
                "detail": "Object already exists",
            },
        )
    except Exception:
        raise HTTPException(
            500,
            detail={
                "status": "failed",
                "data": None,
                "detail": "Internal server error, contact support",
            },
        )
    else:
        return {
            "status": "success",
            "data": operation,
            "detail": None,
        }
