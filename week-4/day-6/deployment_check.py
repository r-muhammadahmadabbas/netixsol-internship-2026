"""
Day 6: Deployment Readiness
Docker, FastAPI, environment variables, health checks
"""
import os
import sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

def check_deployment_readiness():
    print("Checking Deployment Readiness...")
    print("=" * 50)
    
    checks = []
    
    # Check Dockerfile
    dockerfile_exists = os.path.exists("C:/Internship/Netixsol/week-4/Dockerfile")
    checks.append(("Dockerfile", dockerfile_exists))
    print(f"[{'PASS' if dockerfile_exists else 'FAIL'}] Dockerfile")
    
    # Check docker-compose
    compose_exists = os.path.exists("C:/Internship/Netixsol/week-4/docker-compose.yml")
    checks.append(("docker-compose.yml", compose_exists))
    print(f"[{'PASS' if compose_exists else 'FAIL'}] docker-compose.yml")
    
    # Check .env
    env_exists = os.path.exists("C:/Internship/Netixsol/week-4/.env")
    checks.append((".env", env_exists))
    print(f"[{'PASS' if env_exists else 'FAIL'}] .env")
    
    # Check API
    try:
        from api import app
        api_ok = True
    except:
        api_ok = False
    checks.append(("FastAPI", api_ok))
    print(f"[{'PASS' if api_ok else 'FAIL'}] FastAPI")
    
    # Check requirements
    req_exists = os.path.exists("C:/Internship/Netixsol/week-4/requirements.txt")
    checks.append(("requirements.txt", req_exists))
    print(f"[{'PASS' if req_exists else 'FAIL'}] requirements.txt")
    
    passed = sum(1 for _, ok in checks if ok)
    print(f"\nDeployment Readiness: {passed}/{len(checks)}")
    return passed == len(checks)

if __name__ == "__main__":
    check_deployment_readiness()