# main.py

import typer
import os
import subprocess

app = typer.Typer()


@app.command()
def run_backend(host: str = "0.0.0.0", port: int = 8000):
    """
    Starts the FastAPI backend server using Uvicorn.
    """
    print(f"🚀 Starting backend server at http://{host}:{port}")
    # Use subprocess.run to have more control and see output in real-time
    subprocess.run(
        ["uvicorn", "backend.app.main:app", "--host", host, "--port", str(port), "--reload"],
        check=True
    )


@app.command()
def init_db():
    """
    Initializes the database by running the init_db.py script.
    """
    print("🛠️  Initializing database...")
    script_path = os.path.join("scripts", "init_db.py")
    subprocess.run([sys.executable, script_path], check=True)


@app.command()
def seed_db():
    """
    Seeds the database with dummy users and data.
    """
    print("🌱 Seeding database with dummy data...")
    # Run the user generation script first
    print(" -> Generating users...")
    user_script_path = os.path.join("scripts", "generate_dummy_users.py")
    subprocess.run([sys.executable, user_script_path], check=True)

    # Run the data seeding script
    print(" -> Seeding waste and products...")
    seed_script_path = os.path.join("scripts", "seed_data.py")
    subprocess.run([sys.executable, seed_script_path], check=True)

    print("✅ Database seeding complete.")


if __name__ == "__main__":
    app()