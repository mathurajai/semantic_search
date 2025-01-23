import time
from typing import Callable, Any
from app.logging_config import get_logger

# Get the logger
logger = get_logger(__name__)

def measure_time(func: Callable[..., Any]) -> Callable[..., Any]:
    """
    Decorator to measure the execution time of a function.
    
    Args:
    func (Callable[..., Any]): The function to measure.
    
    Returns:
    Callable[..., Any]: The wrapped function with execution time measurement.
    """
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        logger.info(f"Execution time of {func.__name__}: {execution_time:.6f} seconds")
        return result
    
    return wrapper