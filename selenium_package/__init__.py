"""
Selenium Package - A Python package for Selenium automation with action and executor patterns.

This package provides base classes for creating Selenium actions and executors,
following a clean architecture pattern for web automation.
"""

from .interfaces.base_action import BaseAction
from .interfaces.base_executor import BaseExecutor
from .interfaces.exceptions.exceptions import (
    SeleniumBaseActionException,
    SeleniumBaseGetterException,
    MaximumAttemptsReachedException,
    NoMorePagesException,
)

__version__ = "0.1.0"
__author__ = "João Gabriel Sampaio de Barros"
__email__ = "jgabrielsb2002@gmail.com"

__all__ = [
    "BaseAction",
    "BaseExecutor",
    "SeleniumBaseActionException",
    "SeleniumBaseGetterException",
    "MaximumAttemptsReachedException",
    "NoMorePagesException",
]
