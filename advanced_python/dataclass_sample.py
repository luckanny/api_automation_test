import operator
from dataclasses import dataclass, field


@dataclass(order=True)
class Student:
    sort_index: int = field(init=False, repr=False)
    name: str
    school: str
    age: int
    independent: bool = field(default=False, init=False)

    def __post_init__(self):
        self.independent = self.age >= 18
        self.sort_index = self.age



s1 = Student("anny", "primariy", 18)
s2 = Student("steven", "primariy", 17)
s = [s1, s2]
sorted_s = sorted(s)
print(sorted_s)

s.sort(key=operator.attrgetter('name'))
print(s)
