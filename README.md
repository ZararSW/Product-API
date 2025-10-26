# Product CRUD API + Tests

This project provides a minimal FastAPI service implementing CRUD operations for a `Product` entity, along with automated Python tests and a Postman collection for manual verification.

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

## Run tests

You can run tests directly; they will auto-start the API server locally for the session:

```powershell
. .venv\Scripts\Activate.ps1
pytest -q
```

To point tests at a different server, override the base URL:

```powershell
$env:BASE_URL = "http://127.0.0.1:8000"; pytest -q
```

## CLI client (no Postman needed)

You can interact with the API from the command line via a small client:

```powershell
# Health
python -m src.cli health

# Create
python -m src.cli create --name "Sample" --price 9.99 --quantity 5

# List
python -m src.cli list

# Get by ID
python -m src.cli get --id 1

# Update
python -m src.cli update --id 1 --name "Updated" --price 19.99 --quantity 10

# Delete
python -m src.cli delete --id 1
```

Override base URL with an environment variable or flag:

```powershell
$env:BASE_URL = "http://127.0.0.1:8000"; python -m src.cli list
python -m src.cli --base-url http://127.0.0.1:8000 list
```

## PowerShell curl/Invoke-RestMethod examples

```powershell
# Create
$body = @{ name = "Sample"; price = 9.99; quantity = 5 } | ConvertTo-Json
Invoke-RestMethod -Uri http://127.0.0.1:8000/products -Method Post -ContentType "application/json" -Body $body

# List
Invoke-RestMethod -Uri http://127.0.0.1:8000/products -Method Get

# Get by ID
Invoke-RestMethod -Uri http://127.0.0.1:8000/products/1 -Method Get

# Update (full payload required)
$ubody = @{ name = "Updated"; price = 19.99; quantity = 10 } | ConvertTo-Json
Invoke-RestMethod -Uri http://127.0.0.1:8000/products/1 -Method Put -ContentType "application/json" -Body $ubody

# Delete
Invoke-RestMethod -Uri http://127.0.0.1:8000/products/1 -Method Delete -SkipHttpErrorCheck
```

Note: In PowerShell, the `curl` alias points to `Invoke-WebRequest`. If you prefer the cURL executable, use `curl.exe` explicitly.

## Notes

- Data is stored in-memory; restarting the server clears all data.
- This project demonstrates: CRUD endpoints, proper status codes (201/200/204/404), validation errors (422), and automated tests for happy paths and error handling.
