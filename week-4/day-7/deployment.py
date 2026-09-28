"""
Day 7: Production Deployment
Docker, FastAPI, environment setup
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

DEPLOYMENT_CONFIG = {
    "api": {
        "host": "0.0.0.0",
        "port": 8000,
        "workers": 4,
        "reload": False
    },
    "streamlit": {
        "port": 8501,
        "address": "0.0.0.0"
    },
    "docker": {
        "api_image": "realestate-api:latest",
        "ui_image": "realestate-ui:latest",
        "restart_policy": "unless-stopped"
    },
    "environment": {
        "required": ["GROQ_API_KEY"],
        "optional": ["DEEPGRAM_API_KEY", "GOOGLE_CALENDAR_CREDENTIALS", "GMAIL_CREDENTIALS"]
    }
}

def print_deployment_info():
    print("Production Deployment Config:")
    print("=" * 50)
    print(f"API: {DEPLOYMENT_CONFIG['api']['host']}:{DEPLOYMENT_CONFIG['api']['port']}")
    print(f"UI: port {DEPLOYMENT_CONFIG['streamlit']['port']}")
    print(f"Required env vars: {DEPLOYMENT_CONFIG['environment']['required']}")
    print(f"Optional env vars: {DEPLOYMENT_CONFIG['environment']['optional']}")
    print("\nCommands:")
    print("  docker-compose up -d")
    print("  docker-compose logs -f")
    print("  docker-compose down")

if __name__ == "__main__":
    print_deployment_info()