# Star Wars App

A Dockerized microservices application featuring a frontend built with Next.js and Tailwind CSS, and a backend built
with Python FastAPI. The app fetches Star Wars data from an external API and demonstrates TDD practices across both
services.

Visit on AWS: http://starwars-alb-1097306309.eu-central-1.elb.amazonaws.com

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
- **Data Source:** Fetches Star Wars data from [awapi.info/api](https://swapi.info/api)
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
  ### Frontend
- Frontend source code lives in **/frontend**

  #### To enable hot reload during development and run the application using Docker Compose, use the development compose file:
    In root directory:
     ```
    docker compose -f docker-compose.dev.yml up
     ```   
  ### Frontend Dev practice
  
  #### Add dependency locally (in /frontend):
    ```aiignore
    cd frontend/
    npm install something
    ```
  #### Rebuild container after adding dependencies (in root):
    ```
    cd ../ 
    docker compose -f docker-compose.dev.yml build
    ```
  #### Bring it back up:
    ```aiignore
    docker compose -f docker-compose.dev.yml up
    ```
  
### Backend
- Backend source code lives in **/backend**

  #### Start backend with (optional)
    ```
    cd backend/
    uvicorn app.main:app --reload
    ```
  
  
### Docker
- Dockerfiles handle building production-ready containers for each service

  ### Optional: Clean Up Orphan Containers
  ```aiignore
  docker compose -f docker-compose.dev.yml down --remove-orphans
  ```
  or
   ```aiignore
    docker compose -f docker-compose.yml down --remove-orphans
  ```

### Nginx

  Run with:

  ```
  docker compose up -d
  ```
  
  Check logs with:
  ```aiignore
  docker compose logs -f nginx backend frontend
  ```
  
  Check container health with:
  ```
  docker ps
  ```
  
  Start Nginx manually (if needed)
  ```aiignore
  docker start -ai starwars-nginx
  ```
 Run nginx container with that network explicitly (if needed)
  ```
  docker run --rm -p 6969:80 \
  --network star-wars-app_starwars-net \
  -v $(pwd)/nginx/nginx.conf:/etc/nginx/nginx.conf:ro \
  nginx:stable-alpine
  ```

  
  Test endpoints on ports:
  
  http://localhost:6969 (nginx)
  
  http://localhost:8000/api/health (backend)
  
  http://localhost:3000 (frontend)

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

- **External API:** swapi.info/api

---
License
MIT © zlu
