# Microservices Architecture with Custom Eureka Server & FastAPI

A laboratory project demonstrating microservice discovery, registration, and inter-service communication using a custom Eureka Server mock, FastAPI microservices, and Docker Compose.

---

## 🚀 Tech Stack

* **Backend Framework:** Python, FastAPI, Uvicorn
* **Service Discovery:** Custom Eureka Server Mock (FastAPI + XML Registry)
* **Containerization:** Docker, Docker Compose
* **Orchestration & Monitoring:** Portainer CE

---

## 📂 Project Structure

```text
lab_eurika/
│
├── eureka-server/       # Custom Eureka Server mock (handles registration & heartbeats)
├── user-service/        # Microservice 1 (User management, registered via Eureka)
├── order-service/       # Microservice 2 (Order management, registered via Eureka)
└── docker-compose.yml   # Docker Compose configuration for local deployment
