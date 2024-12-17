from sqlalchemy.orm import Session
from app.db.models import Network
from app.schemas.network import NetworkCreate


def create_network(db: Session, network_data: NetworkCreate):
    network = Network(**network_data)
    db.add(network)
    db.commit()
    db.refresh(network)
    return network


def get_network_by_id(db: Session, network_id: str):
    return db.query(Network).filter(Network.id == network_id).first()


def get_network_by_cidr(db: Session, cidr: str):
    return db.query(Network).filter(Network.cidr == cidr).first()


def get_network_by_name(db: Session, name: str):
    return db.query(Network).filter(Network.name == name).first()


def get_all_networks(db: Session):
    return db.query(Network).all()
