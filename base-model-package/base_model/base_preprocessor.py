class BasePreprocess:
    """
    Base class for preprocessing audio data.

    This class provides a template for preprocessing audio waveforms.
    Subclasses should implement the `process` method to define specific
    preprocessing logic.
    """

    def __init__(self) -> None:
        """
        Initialize the Preprocess class.
        """
        pass

    def process(self, wave: list[float]) -> None:
        """
        Process the input audio waveform.

        :param wave: A list of float values representing the audio waveform.
        :raises NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError("Subclasses must implement the `process` method.")