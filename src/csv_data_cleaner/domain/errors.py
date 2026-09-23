"""Domain errors for expected CSV Data Cleaner failures."""


class DataCleanerError(Exception):
    """Base error for expected CSV Data Cleaner failures."""


class InputDataError(DataCleanerError):
    """Raised when an input data file cannot satisfy the input contract."""


class ConfigurationError(DataCleanerError):
    """Raised when a configuration file cannot satisfy the config contract."""


class OutputDataError(DataCleanerError):
    """Raised when output artifacts cannot be written safely."""
