from app.database import clear_database

if __name__ == "__main__":
    print("Clearing database...")
    clear_database()
    print("Database cleared. You can now restart the application to test the caching system.") 