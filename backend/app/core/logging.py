import logging
import sys
from app.core.config import get_settings

def configure_logging():
    """
    Configures the logging for the application.
    Sets the log level based on the DEBUG setting.
    """
    settings = get_settings()
    
    # Determine log level
    log_level = logging.DEBUG if settings.DEBUG else logging.INFO
    
    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    
    # Remove existing handlers to avoid duplicates
    if root_logger.handlers:
        root_logger.handlers = []
        
    root_logger.addHandler(console_handler)
    
    # Set level for specific libraries if needed (e.g., uvicorn)
    logging.getLogger("uvicorn.access").setLevel(log_level)
