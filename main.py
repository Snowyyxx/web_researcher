from dotenv import load_dotenv
import uvicorn
from termcolor import colored

def log_info(message: str) -> None:
    print(colored(f"[INFO] {message}", "yellow"))

def log_success(message: str) -> None:
    print(colored(f"[SUCCESS] {message}", "green"))

if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    
    log_info("Starting Research Assistant server...")
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True
    )
    log_success("Server is running at http://127.0.0.1:8000") 