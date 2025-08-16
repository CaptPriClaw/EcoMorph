# ml-services/ai_registry/ai_engine.py

# --- Import individual AI/ML module classes ---
# These paths assume your ml-services directory is a Python package.
from ..residual_classifier.inference import ResidualClassifier
from ..recommender_system.recommender import Recommender
from ..design_generator.generator import DesignGenerator
from ..credit_predictor.predictor import CreditPredictor  # Assuming predictor logic is in predictor.py


class AIEngine:
    """
    The master AI engine that loads all models and provides a single
    interface to access their functionalities.
    """

    def __init__(self):
        """
        Initializes the AI Engine by loading all necessary models into memory.
        This is done once when the engine is created to ensure fast inference times.
        """
        print("Initializing AI Engine... 🧠")
        # Load each model service. The paths to model files (e.g., model.pkl)
        # will be handled within each class's __init__ method.
        self.classifier = ResidualClassifier()
        self.recommender = Recommender()
        self.design_generator = DesignGenerator()
        self.credit_predictor = CreditPredictor()
        print("AI Engine Ready.")

    def classify_waste_material(self, image_data):
        """
        Takes image data and classifies it as 'residual' or 'usable'.

        Args:
            image_data: The image data (e.g., bytes from an uploaded file).

        Returns:
            A dictionary with the classification result, e.g., {'class': 'usable', 'confidence': 0.95}.
        """
        return self.classifier.run_inference(image_data)

    def recommend_upcycling_ideas(self, waste_description: str, top_n: int = 3):
        """
        Recommends upcycling product ideas based on a text description of waste.

        Args:
            waste_description (str): A text string like "plastic milk jug" or "old cotton t-shirt".
            top_n (int): The number of top recommendations to return.

        Returns:
            A list of recommended product ideas, e.g., ["bird feeder", "watering can", "storage container"].
        """
        return self.recommender.recommend(waste_description, top_n=top_n)

    def generate_product_design(self, waste_material: str, style: str = "modern"):
        """
        Generates a textual or visual design concept for an upcycled product.

        Args:
            waste_material (str): The material to use, e.g., "denim jeans".
            style (str): The desired aesthetic style, e.g., "rustic", "minimalist".

        Returns:
            A dictionary containing the generated design, e.g.,
            {'title': 'Modern Denim Wall Organizer', 'description': '...', 'steps': [...]}.
        """
        return self.design_generator.generate(waste_material, style)

    def predict_credit_exchange_rate(self, market_conditions: dict):
        """
        Predicts the exchange rate between EcoPoints and real-world credits.

        Args:
            market_conditions (dict): A dictionary of features like
                                      {'material_demand': 0.8, 'waste_supply': 0.6, 'time_of_year': 7}.

        Returns:
            The predicted exchange rate, e.g., {'predicted_rate': 125.5}.
        """
        return self.credit_predictor.predict(market_conditions)


# --- Singleton Instance ---
# This creates a single, shared instance of the AIEngine that can be
# imported and used by your API layer, preventing models from being loaded
# multiple times.
ai_engine_instance = AIEngine()