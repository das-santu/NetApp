# NetApp: FastAPI-Based Network and Subnet Management API

## Project Overview
This project is a RESTful API built using **FastAPI** to manage networks and subnets. It includes features for:
1. **User Authentication**: Secure login using JWT tokens with access and refresh token support.
2. **Network Management**: Create, list, and reserve networks.
3. **Subnet Management**: Reserve and calculate subnets within a specified network.
4. **Swagger UI**: API documentation with easy-to-use interactive endpoints.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [API Endpoints](#api-endpoints)
  - [Auth](#auth)
  - [Network](#network)
  - [Subnet](#subnet)
- [Testing](#testing)
- [License](#license)
- [Author](#author)
- [Contribution](#contribution)

## Features
- **User** Management.
- **JWT Authentication** with refresh token.
- **Network Management**: Reserve and manage networks.
- **Subnet Management**: Automatic reservation, usage tracking, and description support.
- **Subnet Calculator**: On-the-fly subnet calculations.
- **Swagger UI**: Interactive API documentation.
- Built with FastAPI, SQLAlchemy, and PostgreSQL.

### Prerequisites
- Python 3.11+
- PostgreSQL 16.0+
- Uvicorn
- Docker 
- Make 4.0+

## Installation
#### 1. Clone the Repository:
```bash
git clone https://github.com/das-santu/NetApp.git
cd NetApp
```

#### 2. Create virtual environment and install dependencies:
```bash
make setup
```

#### 3. Set up environment variables:
Create a .env file in the project root and add the necessary environment variables:

```bash
DATABASE_URL=postgresql://user:password@localhost/dbname
SECRET_KEY="access_secret_key"
REFRESH_SECRET_KEY="refresh_secret_key"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30
REFRESH_TOKEN_EXPIRE_DAYS=7
```

#### 4. Apply Database Migrations:
```bash
make migrate
```

#### 5. Run the development server:
```bash
make run
```

#### 6. Access Swagger UI:
- Swagger Docs: http://127.0.0.1:8000/docs

## API Endpoints
### Auth:
- POST /auth/register - Register new user.
- POST /auth/login - Login and get tokens.
- POST /auth/refresh - Refresh access token.

### Network:
- POST /api/v1/networks/ - Create or reserve a network.
- GET /api/v1/networks/ - List all networks.

### Subnet:
- POST /api/v1/subnets/ - Reserve a free subnet within a network.
- GET /api/v1/subnets/{network_id}/ - List Subnets By Network
- POST /api/v1/subnets/calculator/ - Subnets Calculate API

## Testing

### Run unit tests:
```bash
make test
```

## License
This project is licensed under the MIT License - see the LICENSE file for details.

## Author
Santu Das - [LinkedIn](https://www.linkedin.com/in/santu-das-73388013a) | [GitHub](https://github.com/das-santu)

## Contribution
Contributions are welcome! Feel free to fork this repository and create a pull request. Please ensure your changes are tested and well-documented.
