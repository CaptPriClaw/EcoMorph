# System Architecture

EcoMorph is designed using a modern, scalable, multi-tier architecture that separates concerns for maintainability and independent development.


## 1. Frontend (Client-Side)

- **Framework**: React (using Vite for a fast development experience).
- **Responsibility**: This is the presentation layer. It handles all user interface elements, state management (using Context API or Redux), and communication with the backend via REST API calls. It's a Single Page Application (SPA).

## 2. Backend (Server-Side)

- **Framework**: FastAPI (Python).
- **Responsibility**: This is the application's core logic layer. It handles business logic, data processing, user authentication, and serving data to the frontend.
- **Internal Structure**:
    - `main.py`: The entry point that ties everything together.
    - `routes/`: Defines the API endpoints (`/users`, `/products`, etc.).
    - `services/`: Contains the core business logic (e.g., how a purchase works).
    - `schemas/`: Defines the data shapes for API requests and responses (Pydantic).
    - `models/`: Defines the database table structures (SQLAlchemy ORM).
    - `database.py`: Handles the database connection and sessions.
    - `config.py`: Manages environment variables and application settings.

## 3. ML Services (Intelligence Layer)

- **Technology**: Can be a collection of Python scripts or separate microservices.
- **Responsibility**: This layer houses all the AI/ML models. The main backend communicates with this layer via internal API calls to perform tasks like:
    - Classifying waste materials.
    - Recommending upcycling projects.
    - Generating product design ideas.

## 4. Database (Persistence Layer)

- **Technology**: PostgreSQL (for production) or SQLite (for development).
- **Responsibility**: This layer is responsible for the persistent storage of all application data, including users, products, transactions, and waste items. SQLAlchemy acts as the Object-Relational Mapper (ORM), translating Python objects into database table rows.