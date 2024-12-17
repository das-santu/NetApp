from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.network import NetworkCreate, NetworkResponse, NetworkUtilizationResponse
from app.db.crud.network import create_network, get_all_networks, get_network_by_cidr, get_network_by_name
from app.db.crud.user import get_user_by_username_or_email
from app.core.security import get_current_user
from app.db.crud.network import get_network_by_id
from app.db.crud.subnet import get_subnets_by_network
from app.utils.network import calculate_network_utilization
from copy import copy

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post("/", response_model=NetworkResponse)
def reserve_network(network_data: NetworkCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):
    existing_network = get_network_by_cidr(db, network_data.cidr)
    existing_network_name = get_network_by_name(db, network_data.name)
    if existing_network:
        raise HTTPException(status_code=400, detail="Network already exists")
    if existing_network_name:
        raise HTTPException(status_code=400, detail="Network name already exists")
    current_user = get_user_by_username_or_email(db, current_user.get("id"))
    network = copy(network_data.dict())
    network["reserved_by"] = current_user.id
    return create_network(db, network)


@router.get("/", response_model=list[NetworkResponse])
def list_networks(db: Session = Depends(get_db)):
    return get_all_networks(db)


@router.get("/{network_id}/utilization", response_model=NetworkUtilizationResponse)
def get_network_utilization(network_id: int, db: Session = Depends(get_db)):
    """
    Calculate the utilization of a specific network.
    Returns reserved and available percentages.
    """
    # Step 1: Fetch the Network
    network = get_network_by_id(db, network_id)
    if not network:
        raise HTTPException(status_code=404, detail="Network not found")

    # Step 2: Fetch Reserved Subnets
    reserved_subnets = get_subnets_by_network(db, network.id)

    # Step 3: Calculate Total and Used IPs and return Calculate Percentages
    return calculate_network_utilization(network, reserved_subnets)
