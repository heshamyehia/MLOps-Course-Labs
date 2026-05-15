"""
Churn Prediction API

Run with:
    litestar --app main:app run --reload
Then open:
    http://localhost:8000/schema/swagger
"""

from litestar import Litestar, get, post
from pydantic import BaseModel

from app.logger_setup import setup_logging
from app.model_utils import predict_churn

logger = setup_logging()


# ---------------------------------------------------------------------------
# data Schema
# ---------------------------------------------------------------------------
class Churndata(BaseModel):
    # TODO 1: Add one field (type float) per feature your model expects
    CreditScore: float
    Geography: str
    Gender: str
    Age: float
    Tenure: float
    Balance: float
    NumOfProducts: float
    HasCrCard: float
    IsActiveMember: float
    EstimatedSalary: float


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------


# TODO 2: Create a GET endpoint at "/" that returns a welcome message
#         Log that the home endpoint was accessed
@get("/")
def home() -> dict[str, str]:
    logger.info("Home endpoint accessed")
    return {"message": "Welcome to the Churn Prediction API!"}


# TODO 3: Create a GET endpoint at "/health" that returns {"status": "healthy"}
@get("/health")
def health() -> dict[str, str]:
    return {"status": "healthy"}


# TODO 4: Create a POST endpoint at "/predict" that:
#         - Accepts a Churndata as the data parameter
#         - Extracts features into a list
#         - Calls predict_churn(features)
#         - Returns the prediction
#         - Logs the input features and the prediction result
@post("/predict")
def predict(request: Churndata) -> dict[str, int]:
    features = [
        request.CreditScore,
        request.Geography,
        request.Gender,
        request.Age,
        request.Tenure,
        request.Balance,
        request.NumOfProducts,
        request.HasCrCard,
        request.IsActiveMember,
        request.EstimatedSalary,
    ]
    prediction = predict_churn(features)
    logger.info(f"Input features: {features}")
    logger.info(f"Prediction: {prediction}")
    return {"prediction": prediction}


# ---------------------------------------------------------------------------
# App
# ---------------------------------------------------------------------------
# TODO 5: Register your endpoint functions in the list below
app = Litestar(
    route_handlers=[home, health, predict],
)
