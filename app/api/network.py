from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.network import NetworkCreate, NetworkResponse
from app.db.crud.network import create_network, get_all_networks, get_network_by_cidr
from app.core.security import get_current_user

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post("/", response_model=NetworkResponse)
def reserve_network(network_data: NetworkCreate, db: Session = Depends(get_db)):
    existing_network = get_network_by_cidr(db, network_data.cidr)
    if existing_network:
        raise HTTPException(status_code=400, detail="Network already exists")
    return create_network(db, network_data)


@router.get("/", response_model=list[NetworkResponse])
def list_networks(db: Session = Depends(get_db)):
    return get_all_networks(db)
