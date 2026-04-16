import numpy as np
from sklearn.linear_model import LinearRegression
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RiskEngine:
    """
    A simple risk engine using Linear Regression to calculate a financial risk score.
    In a real scenario, this would be trained on historical financial data.
    """
    def __init__(self):
        # Mock training data: [market_volatility, debt_to_income, credit_utilization]
        X = np.array([
            [0.1, 0.2, 0.1],
            [0.5, 0.5, 0.6],
            [0.9, 0.8, 0.9],
            [0.2, 0.3, 0.2],
            [0.7, 0.6, 0.7]
        ])
        # Mock risk scores (0 to 100)
        y = np.array([10, 55, 95, 25, 75])
        
        self.model = LinearRegression()
        self.model.fit(X, y)
        logger.info("RiskEngine: Linear Regression model initialized.")

    def calculate_score(self, volatility: float, debt_ratio: float, utilization: float) -> float:
        """
        Calculates a risk score based on input parameters.
        """
        try:
            input_data = np.array([[volatility, debt_ratio, utilization]])
            prediction = self.model.predict(input_data)[0]
            # Clip prediction between 0 and 100
            score = max(0, min(100, float(prediction)))
            logger.info(f"RiskEngine: Calculated score {score:.2f} for inputs {[volatility, debt_ratio, utilization]}")
            return score
        except Exception as e:
            logger.error(f"RiskEngine Error: {e}")
            return 50.0  # Default moderate risk on error
