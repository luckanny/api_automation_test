from enum import Enum, unique
from functools import total_ordering


@unique
class ValidationResult(Enum):
    UNKNOWN = 0
    PASS = 1
    FAILED = 2

    def __str__(self):
        return f"{self.name}({self.value})"

    def __eq__(self, other):
        if isinstance(other, int):
            return self.value == other

        if isinstance(other, str):
            return self.name == other.upper()

        if isinstance(other, ValidationResult):
            return self is other

        return False


@total_ordering
class WorkFlowStatus(Enum):
    OPEN = 1
    IN_PROGRESS = 2
    REVIEW = 3
    COMPLETE = 4

    def __lt__(self, other):
        if isinstance(other, int):
            return self.value < other

        if isinstance(other, WorkFlowStatus):
            return self.value < WorkFlowStatus.value

        return False


class ValidationInfo:
    pass


if __name__ == '__main__':
    print(ValidationResult.PASS)
    print(ValidationResult.PASS == 1)
