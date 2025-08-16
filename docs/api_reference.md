# API Reference

This project uses FastAPI, which automatically generates interactive API documentation from the code. This is the best and most up-to-date source for API reference.

## Documentation Endpoints

Once you have the backend server running, you can access the documentation at the following URLs:

### Swagger UI (Interactive)

- **URL**: `http://127.0.0.1:8000/docs`
- **Best for**: Trying out the API endpoints directly from your browser. You can send requests and see live responses.


### ReDoc (Reference)

- **URL**: `http://127.0.0.1:8000/redoc`
- **Best for**: A clean, readable, reference-style view of the API, showing all models, fields, and endpoints in a single page.

## Quick Endpoint Overview

- `POST /token`: User login.
- `POST /users/`: User registration.
- `GET /users/me`: Get current user's profile.
- `POST /waste/`: Submit a new waste item.
- `GET /waste/my-submissions`: View your waste submissions.
- `GET /marketplace/`: Browse available products.
- `POST /marketplace/buy/{product_id}`: Purchase a product.
- `GET /points/my-balance`: Check your EcoPoint balance.
- `GET /points/my-history`: View your points transaction history.