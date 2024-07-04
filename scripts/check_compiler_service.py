import logging
import requests

# Configure logging
logger = logging.getLogger(__name__)

def check_compiler_service():
    """
    Function to check if the compiler service is running.
    """
    try:
        response = requests.get('http://compiler:8001/compiler/health/')
        if response.status_code == 200:
            return True
    except requests.RequestException as e:
        logger.error(f"Compiler service check failed: {e}")
    return False

if __name__ == "__main__":
    if check_compiler_service():
        print("Compiler service is running.")
    else:
        print("Compiler service is not running.")
