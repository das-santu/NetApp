from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.schemas.subnet import SubnetCreate, SubnetResponse, SubnetCalculator
from app.db.crud.subnet import create_subnet, get_subnets_by_network
from app.db.crud.network import get_network_by_id
from app.db.crud.user import get_user_by_username_or_email
from app.utils.subnet import calculate_subnets, find_free_subnet
from app.core.security import get_current_user

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.post("/", response_model=SubnetResponse)
def reserve_subnet(payload: SubnetCreate, db: Session = Depends(get_db), current_user: dict = Depends(get_current_user)):

    # 1. Retrieve the parent network
    network = get_network_by_id(db, payload.network_id)
    if not network:
        raise HTTPException(status_code=404, detail="Network not found")

    # 2. Retrieve existing subnets for this network
    existing_subnets = get_subnets_by_network(db, network.id)

    # 3. Find a free subnet based on the prefix
    free_subnet = find_free_subnet(network.cidr, existing_subnets, payload.prefix)
    if not free_subnet:
        raise HTTPException(status_code=400, detail="No available subnet found")

    current_user = get_user_by_username_or_email(db, current_user.get("sub"))

    # 4. Reserve the subnet
    new_subnet = {
        "network_id": network.id,
        "subnet": free_subnet,
        "reserved_by": current_user.id,
        "description": payload.description,
        "usage": payload.usage,
    }
    return create_subnet(db, new_subnet)


@router.get("/{network_id}/", response_model=list[SubnetResponse])
def list_subnets_by_network(network_id: int, db: Session = Depends(get_db)):
    return get_subnets_by_network(db, network_id)


@router.post("/calculator/")
def calculate_subnets_api(network_data: SubnetCalculator):
    try:
        subnets = calculate_subnets(network_data.network_cidr, network_data.prefix_length)
        return {"subnets": subnets}
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
