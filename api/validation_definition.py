from enum import Enum, unique
from dataclasses import dataclass
from abc import ABC, abstractmethod


@unique
class ValidationStatus(Enum):
    UNKNOWN = 0
    PASS = 1
    FAILED = 2


@dataclass
class ValidationResult:
    status: ValidationStatus
    message: str = ""


class ValidationRule(ABC):

    @abstractmethod
    def validation_rule(self, rule_params, resp, *args):
        pass

