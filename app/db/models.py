from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)

    reserved_networks = relationship("Network", back_populates="reserved_user")
    reserved_subnets = relationship("Subnet", back_populates="reserved_user")


class Network(Base):
    __tablename__ = "networks"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    cidr = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    usage = Column(String, nullable=True)
    reserved_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    reserved_user = relationship("User", back_populates="reserved_networks")
    subnets = relationship("Subnet", back_populates="network")


class Subnet(Base):
    __tablename__ = "subnets"

    id = Column(Integer, primary_key=True, index=True)
    network_id = Column(Integer, ForeignKey("networks.id"), nullable=False)
    subnet = Column(String, unique=True, nullable=False)
    description = Column(String, nullable=True)
    usage = Column(String, nullable=True)
    reserved_by = Column(Integer, ForeignKey("users.id"), nullable=True)

    reserved_user = relationship("User", back_populates="reserved_subnets")
    network = relationship("Network", back_populates="subnets")
