from fastapi import FastAPI
from app.db.base import Base
from app.db.session import engine
from app.api import auth, network, subnet

# # Define the token URL for login
# oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

app = FastAPI(title="NetApp", description="API Documentation", version="1.0.0")

# Create tables
Base.metadata.create_all(bind=engine)

# Include routers
app.include_router(auth.router, prefix="/auth", tags=["Auth"])
app.include_router(network.router, prefix="/api/v1/networks", tags=["Networks"])
app.include_router(subnet.router, prefix="/api/v1/subnets", tags=["Subnets"])
