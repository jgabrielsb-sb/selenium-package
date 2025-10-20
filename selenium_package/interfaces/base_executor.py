from abc import ABC, abstractmethod

from .base_action import BaseAction
from ..messages import *

from typing import Any

from selenium.webdriver.remote.webelement import WebElement

import time

class BaseExecutor(ABC):
    def __init__(
        self, 
        action: BaseAction,
        web_element: WebElement = None,
        wait_to_verify_condition: int = None,
        timeout: int = 30,
    ):
        if not isinstance(action, BaseAction):
            raise ValueError(
                VARIABLE_MUST_BE_A_BASE_ACTION_INSTANCE.format(
                    variable_name='action'
                )
            )

        if web_element is not None and not isinstance(web_element, WebElement):
            raise ValueError(
                VARIABLE_MUST_BE_A_WEB_ELEMENT_INSTANCE.format(
                    variable_name='web_element'
                )
            )

        if wait_to_verify_condition is not None:
            if not isinstance(wait_to_verify_condition, int) or wait_to_verify_condition <= 0:
                raise ValueError(
                    VARIABLE_MUST_BE_AN_INTEGER_GREATER_THAN_0.format(
                        variable_name='wait_to_verify_condition'
                    )
                )

        
        if not isinstance(timeout, int) or timeout <= 0:
            raise ValueError(
                VARIABLE_MUST_BE_AN_INTEGER_GREATER_THAN_0.format(
                    variable_name='timeout'
                )
            )

        self.action = action
        self.web_element = web_element
        self.wait_to_verify_condition = wait_to_verify_condition
        self.timeout = timeout

    @abstractmethod
    def _is_condition_to_stop_met(self, result: Any = None) -> bool:
        pass

    def is_condition_to_stop_met(self, result: Any = None) -> bool:
        if result is not None:
            is_condition_to_stop_met = self._is_condition_to_stop_met(result)
        else:
            is_condition_to_stop_met = self._is_condition_to_stop_met()

        if not isinstance(is_condition_to_stop_met, bool):
            raise ValueError(
                VARIABLE_MUST_BE_A_BOOLEAN.format(  
                    variable_name='is_condition_to_stop_met'
                )
            )

        return is_condition_to_stop_met

    def run(self) -> Any:
        is_condition_to_stop_met = False
        action_result = None

        start_time = time.time()

        while not is_condition_to_stop_met:
            if time.time() - start_time > self.timeout:
                raise TimeoutError(
                    'action timeout: the action took more than {} seconds to complete'.format(
                        self.timeout
                    )
                )
            try:
                action_result = self.action.run()
            except Exception as e:
                pass

            is_condition_to_stop_met = self.is_condition_to_stop_met(action_result)

            # If the condition is not met, re-execute the verification of the condition after the wait time
            if not is_condition_to_stop_met and self.wait_to_verify_condition is not None:
                time.sleep(self.wait_to_verify_condition)
                is_condition_to_stop_met = self.is_condition_to_stop_met(action_result)

        return action_result
