# Product CRUD API 

This project provides a minimal FastAPI service implementing CRUD operations for a `Product` entity.

## API overview

Base URL: `http://127.0.0.1:8000`

- Health: `GET /health` → 200 `{ "status": "ok" }`
- Create: `POST /products` → 201 `{ id, name, price, quantity }`
  - Request JSON: `{ "name": string, "price": number (>=0), "quantity": integer (>=0) }`
- List: `GET /products` → 200 `[{ id, name, price, quantity }, ...]`
- Read: `GET /products/{id}` → 200 `{ id, name, price, quantity }` or 404
- Update: `PUT /products/{id}` → 200 `{ id, name, price, quantity }` or 404
  - Request JSON: same as Create
- Delete: `DELETE /products/{id}` → 204 or 404

Validation errors return 422 with details (FastAPI default).

## Run locally

1. Install dependencies (Python 3.9+ recommended):

```powershell
python -m venv .venv
. .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

2. Start the API:

```powershell
uvicorn src.app:app --host 127.0.0.1 --port 8000 --reload
```

Swagger UI (OpenAPI): http://127.0.0.1:8000/docs



Note: In PowerShell, the `curl` alias points to `Invoke-WebRequest`. If you prefer the cURL executable, use `curl.exe` explicitly.

## Notes

- Data is stored in-memory; restarting the server clears all data.
- This project demonstrates: CRUD endpoints, proper status codes (201/200/204/404), validation errors (422), and automated tests for happy paths and error handling.

