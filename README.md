# Star Wars App

A Dockerized microservices application featuring a frontend built with Next.js and Tailwind CSS, and a backend built
with Python FastAPI. The app fetches Star Wars data from an external API and demonstrates TDD practices across both
services.

---

## Architecture

The app consists of two microservices:

### Frontend

- **Framework:** Next.js 15
- **Styling:** Tailwind CSS
- **Testing:** Vitest (unit tests) and Playwright (end-to-end tests)
- **Function:** Fetches data from the backend API and renders the UI

### Backend

- **Framework:** Python FastAPI
- **Data Source:** Fetches Star Wars data from [awapi.info/api](https://awapi.info/api)
- **Testing:** TDD with unittest and pytest
- **Function:** Provides a REST API consumed by the frontend

---

## Features

- Fully Dockerized with `docker compose`
- Healthchecks implemented for reliable container orchestration
- Separate development and production workflows
- Unit and integration tests with CI pipelines for both frontend and backend
- Easy local development with hot reload and volume mount

--- 

## Getting Started

### Prerequisites

- Docker & Docker Compose installed
- Node.js (for local frontend development if needed)
- Python 3.12+ (for local backend development if needed)

### Run the full app locally with Docker Compose

```
docker compose up --build
```

Frontend accessible at http://localhost:3000

Backend API accessible at http://localhost:8000/api

---

## Running Tests

### Backend tests:

**Linting:**

```aiignore
docker compose run backend flake8 .
```

**Unit tests**:

```
docker compose run backend pytest
```

### Frontend tests:

Run tests locally inside the `frontend/` directory using:

```
cd frontend
```

```
npx vitest
```

## Development

- Frontend source code lives in **/frontend**

  #### To enable hot reload during development and run the application using Docker Compose, use the development compose file:
     ```
    docker compose -f docker-compose.dev.yml up
     ```    
      
- Backend source code lives in **/backend**

- Dockerfiles handle building production-ready containers for each service

---

## CI/CD Pipelines

- Backend CI runs Python tests inside the Docker container

- Frontend CI installs Node dependencies, runs Vitest, then builds the Docker image

- Healthchecks configured for Docker Compose to ensure service readiness

---

## Technologies Used

- **Frontend:** Next.js 15, Tailwind CSS, Vitest, Playwright

- **Backend:** Python, FastAPI, unittest, pytest

- **Docker:** Multi-stage builds, docker-compose

- **External API:** awapi.info

---
License
MIT © zlu
