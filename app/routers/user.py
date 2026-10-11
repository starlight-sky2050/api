from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.orm import Session

from app.core.db import get_db_session
from app.repositories.user import UserRepository
from app.schemas.user import UserCreate, UserResponse, UserUpdate

router = APIRouter(prefix="/api/users", tags=["users"])


@router.post("", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(
    user: UserCreate,
    session: Session = Depends(get_db_session),
) -> UserResponse:
    return UserRepository(session).create(user.model_dump())


@router.get("", response_model=list[UserResponse])
def get_users(session: Session = Depends(get_db_session)) -> list[UserResponse]:
    return UserRepository(session).get_all()


@router.get("/{uid}", response_model=UserResponse)
def get_user(uid: int, session: Session = Depends(get_db_session)) -> UserResponse:
    user = UserRepository(session).get_by_id(uid)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user


@router.patch("/{uid}", response_model=UserResponse)
def update_user(
    uid: int,
    user: UserUpdate,
    session: Session = Depends(get_db_session),
) -> UserResponse:
    updated_user = UserRepository(session).update(
        uid, user.model_dump(exclude_unset=True)
    )
    if updated_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return updated_user


@router.delete("/{uid}", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
def delete_user(uid: int, session: Session = Depends(get_db_session)) -> Response:
    deleted_user = UserRepository(session).delete(uid)
    if deleted_user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)