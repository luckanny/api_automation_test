from api.parse_holder import process_env_holder
from dataclasses import dataclass, field
from typing import List


@dataclass
class Case:
    case_name: str = field(default='')
    section_name: str = field(default='')
    case_steps: List = field(default_factory=[])

    def update_step_list(self, step_content):
        self.case_steps.append(step_content)


@dataclass
class Step:
    step_content: dict
    step_name: str = None

    def __post_init__(self):
        self.step_content = process_env_holder(self.step_content)
        self.step_name = self.step_content["name"]
