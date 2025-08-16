# EcoMorph ♻️

Welcome to EcoMorph, an innovative platform designed to transform waste into value. EcoMorph connects users who have waste materials with creative upcyclers who can turn those materials into new, valuable products. The platform features an AI-powered suggestion engine, a points-based economy, and a vibrant marketplace.

## ✨ Key Features

- **AI-Powered Suggestions**: Upload an image of a waste item and get AI-driven ideas for what it can become.
- **Gamified Points System**: Earn "EcoPoints" for contributing waste materials and participating in the community.
- **Upcycled Marketplace**: Browse and purchase unique, handcrafted products made from upcycled materials using your EcoPoints.
- **Two-Sided Platform**: Caters to both **Uploaders** (who provide raw materials) and **Upcyclers** (who create and sell products).

## 🛠️ Tech Stack

- **Frontend**: React, Vite, CSS Modules
- **Backend**: FastAPI, Python, SQLAlchemy
- **Database**: PostgreSQL (or SQLite for local development)
- **AI / ML**: OpenAI GPT-4, Scikit-learn, Pytorch/TensorFlow
- **Deployment**: Docker, Docker Compose

## 🚀 Getting Started

Follow these instructions to get the backend server up and running on your local machine.

### Prerequisites

- Python 3.9+
- Docker (optional, for running a database)

### Installation

1.  **Clone the repository:**
    ```sh
    git clone [https://github.com/your-username/UpCycleOS.git](https://github.com/your-username/UpCycleOS.git)
    cd UpCycleOS/backend
    ```

2.  **Create a virtual environment:**
    ```sh
    python -m venv venv
    source venv/bin/activate  # On Windows use `venv\Scripts\activate`
    ```

3.  **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

4.  **Set up environment variables:**
    Create a file named `.env` in the `backend/app/` directory and add your settings:
    ```
    DATABASE_URL="sqlite:///./ecomorph.db"
    SECRET_KEY="a-very-secret-key-for-your-project"
    ```

5.  **Run the application:**
    ```sh
    uvicorn app.main:app --reload
    ```

The API will be running at `http://127.0.0.1:8000`.

## 📚 API Documentation

Once the server is running, you can access the interactive API documentation at:

- **Swagger UI**: `http://127.0.0.1:8000/docs`
- **ReDoc**: `http://127.0.0.1:8000/redoc`