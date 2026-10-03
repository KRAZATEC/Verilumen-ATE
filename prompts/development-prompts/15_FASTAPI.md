# Prompt 15 — FastAPI Production API

Implement the backend API for the complete workflow.

## Core flow
Upload CSV → validate/process → dashboard analytics → failure investigation → AI analysis → prediction.

## Endpoints
Provide well-typed endpoints for:
- health/readiness
- upload/session creation
- schema/data-quality profile
- overview/yield analytics
- failure analytics
- visualization aggregates
- investigation by record/device/test/lot/wafer
- anomaly ranking/details
- model/evaluation metadata
- prediction on unseen records
- evidence-grounded AI analysis

Use REST conventions, Pydantic response models, consistent error envelopes, request validation, and configurable limits.

## Sessions
Avoid global mutable state as the only mechanism. Implement a clear session abstraction and document local-development storage. Structure it so persistent storage can be introduced later.

## Security basics
Validate file type/size, avoid path traversal, do not execute uploaded content, sanitize logs, and avoid exposing internal stack traces in production responses.

## Tests
API tests must cover valid upload, invalid upload, empty data, prediction, anomaly lookup, and insufficient-data cases.
