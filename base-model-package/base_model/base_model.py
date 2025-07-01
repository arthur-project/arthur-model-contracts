class BaseModel:
    """
    Base class for machine learning models.

    This class provides a template for loading a model and making predictions.
    Subclasses should implement the `predict` method to define specific
    prediction logic.
    """

    def __init__(self, path_to_model: str) -> None:
        """
        Initialize the BaseModel class.

        :param path_to_model: Path to the model file.
        """
        self.path: str = path_to_model

    def predict(self, wave: list[float], sample_rate: int = 16000) -> list[tuple[str, float]]:
        """
        Make a prediction based on the input audio waveform.

        :param wave: A list of float values representing the audio waveform.
        :param sample_rate: The sample rate of the audio waveform (default is 16000).
        :return: A list of tuples containing words and their probabilities.
        :raises NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError("Subclasses must implement the `predict` method.")