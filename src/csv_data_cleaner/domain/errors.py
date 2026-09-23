"""Domain errors for invalid input and configuration."""


class DataCleanerError(Exception):
    """Base error for expected CSV Data Cleaner failures."""


class InputDataError(DataCleanerError):
    """Raised when an input data file cannot satisfy the input contract."""


class ConfigurationError(DataCleanerError):
    """Raised when a configuration file cannot satisfy the config contract."""
