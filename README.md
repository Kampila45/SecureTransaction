# SecureTransaction API

Production-grade fraud detection API built with FastAPI, following Hexagonal Architecture and Domain-Driven Design principles.

## Features

- **Hexagonal Architecture** with strict dependency inversion
- **Domain-Driven Design** with rich domain models
- **Async/await** throughout for high performance
- **XGBoost/LightGBM** ML model integration for fraud detection
- **PostgreSQL** database with async SQLAlchemy
- **Health checks** with dependency monitoring

## Dataset

The model is trained on the **Credit Card Fraud Detection** dataset from Kaggle:

- **Source:** [Kaggle - Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)
- **Size:** 284,807 transactions (492 fraudulent)
- **Features:** 28 PCA-transformed features + amount + time
- **Format:** CSV
- **Note:** Features are anonymized via PCA for privacy

The training script automatically downloads this dataset using `kagglehub` if available, or falls back to synthetic data for development.

## Quick Start

### Prerequisites

- Python 3.11 or 3.12 (recommended - Python 3.13 may have package compatibility issues)
- [uv](https://github.com/astral-sh/uv) package manager
- PostgreSQL database

**Note:** If using Python 3.13, you may need Visual C++ Build Tools to compile packages from source. Python 3.12 is recommended for best compatibility.

### Installation

1. Install dependencies with uv:
```bash
uv sync
```

3. Create a `.env` file:
```env
DATABASE_URL=postgresql+psycopg://user:password@localhost:5432/fraud_detection
MODEL_PATH=app/adapters/outbound/ml/models/model.pkl
LOG_LEVEL=INFO
```

4. Train the ML model:
```bash
uv run python scripts/train_model.py
```
This creates a trained XGBoost model at `app/adapters/outbound/ml/models/model.pkl`.

The script will automatically use the Kaggle Credit Card Fraud Detection dataset if `creditcard.csv` is present in the project root, or falls back to synthetic data for development.

5. Create the database tables:

6. Start the server:
```bash
uv run uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

- `POST /assess-fraud` - Assess fraud risk for a transaction
- `GET /fraud-decisions/{transaction_id}` - Get fraud decision by transaction ID
- `GET /fraud-decisions/user/{user_id}` - Get fraud history for a user
- `GET /health` - Health check with dependency status
- `GET /docs` - Interactive API documentation (Swagger UI)

## Project Structure

```
app/
├── adapters/
│   ├── inbound/http/          # FastAPI endpoints and models
│   │   ├── endpoints/         # API route handlers
│   │   └── models/           # Request/response models
│   └── outbound/              # Infrastructure adapters
│       ├── persistence/       # Database repositories and models
│       ├── ml/                # ML model loading and scoring
│       └── logging/           # Logging adapter
├── application/
│   └── use_cases/             # Business use case orchestration
├── domain/                    # Core business logic
│   ├── entities/              # Domain entities with behavior
│   ├── value_objects/         # Immutable value objects
│   ├── ports/                 # Repository and service interfaces
│   └── services/              # Domain services
└── composition/               # Dependency injection container

scripts/
└── train_model.py             # ML model training script
```

## Architecture

The system follows **Hexagonal Architecture** (Ports and Adapters):

- **Domain Layer**: Pure business logic, no framework dependencies
- **Application Layer**: Use cases orchestrate domain logic
- **Adapters**: Inbound (HTTP) and outbound (DB, ML) adapters
- **Composition**: Dependency wiring and application startup

## Database Schema

The system uses PostgreSQL with the following tables:

```sql
CREATE TABLE transactions (
    id SERIAL PRIMARY KEY,
    transaction_id VARCHAR NOT NULL UNIQUE,
    user_id VARCHAR NOT NULL,
    merchant_id VARCHAR NOT NULL,
    amount VARCHAR NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    metadata VARCHAR
);

CREATE INDEX idx_transactions_transaction_id ON transactions(transaction_id);
CREATE INDEX idx_transactions_user_id ON transactions(user_id);

CREATE TABLE fraud_decisions (
    id SERIAL PRIMARY KEY,
    transaction_id VARCHAR NOT NULL,
    risk_score FLOAT NOT NULL,
    decision VARCHAR NOT NULL,
    timestamp TIMESTAMP NOT NULL,
    CONSTRAINT fk_fraud_decisions_transaction_id 
        FOREIGN KEY (transaction_id) 
        REFERENCES transactions(transaction_id)
);

CREATE INDEX idx_fraud_decisions_transaction_id ON fraud_decisions(transaction_id);
```

## Development

### Running Tests

```bash
uv run pytest
```

### Type Checking

```bash
uv run mypy app --strict
```

### Code Formatting

```bash
uv run black app
uv run isort app
```

### Environment Variables

- `DATABASE_URL`: PostgreSQL connection string
- `MODEL_PATH`: Path to ML model file
- `LOG_LEVEL`: Logging level (INFO, DEBUG, etc.)

## License

MIT

