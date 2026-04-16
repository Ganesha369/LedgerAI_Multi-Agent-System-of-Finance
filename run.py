import os
import subprocess
import sys
from dotenv import load_dotenv

def check_env():
    """Checks if required environment variables are loaded."""
    load_dotenv()
    required_vars = ["GOOGLE_API_KEY", "PINECONE_API_KEY", "PINECONE_ASSISTANT_HOST"]
    missing = [var for var in required_vars if not os.getenv(var) or "your_" in os.getenv(var)]
    
    if missing:
        print(f"Warning: Missing or placeholder environment variables: {', '.join(missing)}")
        print("Please update your .env file before running in production.")
        return False
    print("Environment variables loaded successfully.")
    return True

def start_server():
    """Starts the FastAPI server using uvicorn."""
    print("Starting Ledger AI FastAPI Server...")
    try:
        # Using subprocess to run uvicorn
        subprocess.run([sys.executable, "-m", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user.")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")

if __name__ == "__main__":
    print("--- Ledger AI Startup Check ---")
    check_env()
    start_server()
