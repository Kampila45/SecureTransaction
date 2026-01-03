# SecureTransaction API

**Machine Learning Fraud Detection System** - A production-grade machine learning API for real-time transaction fraud detection, built with FastAPI, XGBoost, and Hexagonal Architecture.

## What is this?

SecureTransaction API is a **machine learning-based fraud detection system** that uses **supervised learning** to automatically assess the risk of financial transactions in real-time. The system leverages **XGBoost**, a powerful gradient boosting algorithm, to analyze transaction patterns and predict fraudulent activity.

### Use Case

This API is designed for:
- **Payment processors** needing real-time fraud screening
- **E-commerce platforms** protecting against fraudulent transactions
- **Financial services** requiring automated risk assessment
- **Fintech applications** implementing fraud prevention systems

**How it works:**
1. A transaction request is submitted to the API
2. The **ML model** analyzes transaction features (amount, time, metadata)
3. The system calculates a **risk score** (0.0 to 1.0) using the trained model
4. Additional business rules enhance the risk assessment
5. A decision is made: **APPROVE**, **REVIEW**, or **BLOCK**
6. All decisions are stored for audit and historical analysis

## Machine Learning Model

The fraud detection system uses **XGBoost** (Extreme Gradient Boosting), a state-of-the-art machine learning algorithm for supervised learning. The model is trained on historical transaction data to learn patterns that indicate fraudulent behavior.

### Model Architecture

- **Algorithm:** XGBoost (Extreme Gradient Boosting)
- **Type:** Supervised learning classifier
- **Output:** Probability score (0.0 = low risk, 1.0 = high risk)
- **Features Analyzed:**
  - Transaction amount
  - Time of day and day of week
  - User and merchant information
  - Metadata (IP address, device ID, location, payment method)
- **Decision Logic:** 
  - Risk < 0.3 → **APPROVE**
  - Risk 0.3-0.7 → **REVIEW** (manual inspection)
  - Risk > 0.7 → **BLOCK** (high fraud probability)

The model can be retrained with new data to improve accuracy over time.

### Training Dataset

The model is trained on the **Credit Card Fraud Detection** dataset from Kaggle:

- **Source:** [Kaggle - Credit Card Fraud Detection](https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud)
- **Size:** 284,807 transactions (492 fraudulent, ~0.17% fraud rate)
- **Features:** 28 PCA-transformed features + amount + time
- **Format:** CSV
- **Note:** Features are anonymized via PCA for privacy protection

The training script automatically downloads this dataset using `kagglehub` if available, or falls back to synthetic data for development purposes.

## Codebase Features

Key technical features and architectural patterns used in this codebase:

- **Hexagonal Architecture** with strict dependency inversion
- **Domain-Driven Design** with rich domain models
- **Async/await** throughout for high performance
- **XGBoost/LightGBM** ML model integration for fraud detection
- **PostgreSQL** database with async SQLAlchemy
- **Health checks** with dependency monitoring

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

**Note:** The ML model must be trained before the API can make fraud predictions. The training process typically takes a few minutes depending on your hardware.

5. Create the database tables:

6. Start the server:
```bash
uv run uvicorn app.main:app --reload
```

The API will be available at `http://localhost:8000`

## API Endpoints

### Fraud Assessment (ML Prediction)

**`POST /assess-fraud`** - Assess fraud risk for a transaction using machine learning

This endpoint uses the trained ML model to predict fraud probability in real-time.

**Example Request:**
```json
{
  "user_id": "user_12345",
  "merchant_id": "merchant_abc",
  "amount": 150.00,
  "timestamp": "2024-01-15T14:30:00Z",
  "metadata": {
    "ip_address": "192.168.1.1",
    "device_id": "device_xyz",
    "location": "US",
    "payment_method": "credit_card"
  }
}
```

**Example Response:**
```json
{
  "transaction_id": "550e8400-e29b-41d4-a716-446655440000",
  "risk_score": 0.23,
  "decision": "approve",
  "timestamp": "2024-01-15T14:30:01Z"
}
```

### Other Endpoints

- `GET /fraud-decisions/{transaction_id}` - Retrieve fraud decision by transaction ID
- `GET /fraud-decisions/user/{user_id}` - Get fraud history for a user (all past decisions)
- `GET /health` - Health check with dependency status (database, ML model)
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

## How Machine Learning is Used

### Real-Time Fraud Detection Workflow

1. **Transaction Submission**
   - Client sends transaction data via REST API
   - System validates input and creates domain entities

2. **Feature Extraction**
   - Transaction data is transformed into ML model features:
     - Transaction amount (normalized)
     - Time-based features (hour, day of week)
     - Metadata indicators (IP presence, device ID, etc.)

3. **ML Model Prediction**
   - XGBoost model processes features
   - Returns fraud probability score (0.0 - 1.0)
   - Prediction runs asynchronously for performance

4. **Risk Assessment**
   - ML score is combined with business rules:
     - High-value transactions (>$10,000) increase risk
     - Off-hours transactions (2 AM - 6 AM) increase risk
   - Final risk score is calculated

5. **Decision Making**
   - Risk score determines action:
     - **APPROVE**: Low risk, transaction proceeds
     - **REVIEW**: Medium risk, requires manual review
     - **BLOCK**: High risk, transaction rejected

6. **Persistence**
   - Transaction and decision are stored in PostgreSQL
   - Enables audit trails and historical analysis
   - Supports model retraining with new data

### Model Performance

The XGBoost model is evaluated using standard ML metrics:
- **ROC-AUC Score**: Measures model's ability to distinguish fraud from legitimate transactions
- **Classification Report**: Precision, recall, and F1-score for fraud detection
- Model performance is displayed during training

## Architecture

The system follows **Hexagonal Architecture** (Ports and Adapters):

- **Domain Layer**: Pure business logic, no framework dependencies
- **Application Layer**: Use cases orchestrate domain logic
- **Adapters**: Inbound (HTTP) and outbound (DB, ML) adapters
- **Composition**: Dependency wiring and application startup

The ML model is integrated as an **outbound adapter**, keeping the domain layer clean and allowing easy model swapping or updates.

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

