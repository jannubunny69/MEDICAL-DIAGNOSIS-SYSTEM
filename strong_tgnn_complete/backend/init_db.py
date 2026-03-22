"""Create the SQLite database and tables for the backend models.

Run from the project root (PowerShell):
  python backend/init_db.py

This script imports `engine` and `Base` from `backend.models.database` and
calls `Base.metadata.create_all(engine)` which creates the tables defined in
`backend/models/*.py`.
"""
from backend.models import database


def main():
    print("Creating database and tables...")
    # Import models so they are registered with Base.metadata
    # The models live in backend.models package and import Base from database
    try:
        # Importing the models modules ensures their Table metadata is attached to Base
        import backend.models.patient_model  # noqa: F401
        import backend.models.visit_model  # noqa: F401
        import backend.models.result_model  # noqa: F401
    except Exception as e:
        print(f"Warning: couldn't import model modules: {e}")

    database.Base.metadata.create_all(bind=database.engine)
    print("Database created at:", database.DATABASE_URL)


if __name__ == "__main__":
    main()
