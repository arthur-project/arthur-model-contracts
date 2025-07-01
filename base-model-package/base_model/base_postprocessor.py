class BasePostprocess:
    """
    Base class for postprocessing data.

    This class provides a template for postprocessing data after model inference.
    Subclasses should implement the `process` method to define specific
    postprocessing logic.
    """

    def __init__(self) -> None:
        """
        Initialize the BasePostprocess class.
        """
        pass

    def process(self, data: any) -> any:
        """
        Process the input data.

        :param data: The input data to be postprocessed.
        :raises NotImplementedError: If the method is not implemented in a subclass.
        """
        raise NotImplementedError("Subclasses must implement the `process` method.")