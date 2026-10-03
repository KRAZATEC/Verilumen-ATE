# Prompt 01 — Project Foundation

Act as a senior Python/TypeScript staff engineer. Build the foundation of a production-quality repository named `verilumen-ate-intelligence` for the Verilumen Labs AI Engineer assessment.

## Context
The application must help an ATE/test engineer understand semiconductor test results, identify failures/anomalies, make predictions, and explain results. The assessment requires a reusable solution that works when a new CSV with the same schema is supplied.

## Deliverables
Create the complete repository skeleton:
- `backend/app/...` modular service architecture
- `frontend/` Next.js TypeScript application
- `data/`, `models/`, `tests/`, `docs/`, `reports/`, `prompts/`, `docker/`
- `README.md`, `.gitignore`, `.env.example`, `docker-compose.yml`
- backend `pyproject.toml` and requirements strategy
- frontend package configuration

## Backend architecture
Use thin API routes and domain-oriented services:
`data`, `analytics`, `ml`, `anomaly`, `explainability`, `services`, `api`.
Create typed configuration, structured logging, error types, health endpoint, and application factory where appropriate.

## Frontend architecture
Use App Router. Establish a professional ATE engineering dashboard shell with navigation for Overview, Data Quality, Yield & Failures, Investigation, AI Analysis, Prediction, and Settings/About. Do not create fake analytics yet. Empty states must clearly explain that a CSV must be uploaded.

## Quality
Set up Ruff/Black/MyPy/pytest and frontend lint/type checking. Add a basic health test and frontend build/lint configuration.

## Important
Do not implement analytics or ML in this prompt. Establish clean extension points and documentation so later prompts can build on the foundation without restructuring the project.

## Acceptance criteria
- Repository installs cleanly.
- Backend starts and `/health` responds.
- Frontend starts and displays a functional shell.
- Tests pass.
- No fake dataset metrics are shown.
- Architecture is documented.
