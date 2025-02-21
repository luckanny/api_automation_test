from dataclasses import dataclass, field
from typing import List
from common.required_string import RequiredString


# @dataclass
# class Case:
#     case_name: str = RequiredString
#     section_name: str = field(default='')
#     case_steps: List = field(default_factory=[])
#
#     def update_step_list(self, step_content):
#         self.case_steps.append(step_content)

#
# @dataclass
# class Step:
#     step_content: dict
#     step_name: str = None
#
#     def __post_init__(self):
#         self.step_name = self.step_content["name"]


class Case:
    case_name = RequiredString(True)



if __name__ == '__main__':
    case1 = Case()
    case1.case_name = "tom"
    print(case1.case_name)

