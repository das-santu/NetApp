from sqlalchemy.orm import Session
from app.db.models import Subnet
from app.schemas.subnet import SubnetCreate


def create_subnet(db: Session, subnet_data: SubnetCreate):
    subnet = Subnet(**subnet_data)
    db.add(subnet)
    db.commit()
    db.refresh(subnet)
    return subnet


def get_subnets_by_network(db: Session, network_id: int):
    return db.query(Subnet).filter(Subnet.network_id == network_id).all()
