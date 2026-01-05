# app/routes/session.py
from fastapi import APIRouter, Depends, status
from models.session import Session, SessionResponse, SessionUpdate
from controllers.session import create_session, get_sessions_by_car, update_session, get_all_sessions
from utils.security import role_required
from utils.user_type import RoleEnum
from models.user import User

router = APIRouter()

@router.post("/create", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
def create_session_route(session: Session,current_user: User = Depends(role_required([RoleEnum.admin, RoleEnum.client]))):
    return create_session(session)

@router.get("/car/{car_id}",response_model=list[SessionResponse])
def get_sessions_for_car(car_id: str,current_user: User = Depends(role_required([RoleEnum.admin, RoleEnum.client]))):
    return get_sessions_by_car(car_id)

@router.put("update/{session_id}",response_model=SessionResponse)
def update_session_route(session_id: str,data: SessionUpdate,current_user: User = Depends(role_required([RoleEnum.admin, RoleEnum.client]))):
    return update_session(session_id, data)

@router.get("/all", response_model=list[SessionResponse])
def get_all_sessions_route(current_user: User = Depends(role_required(RoleEnum.admin))):
    return get_all_sessions()