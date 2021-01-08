from enum import Enum


class DayName(Enum):
    MONDAY = "poniedziałek"
    TUESDAY = "wtorek"
    WEDNESDAY = "środa"
    THURSDAY = "czwartek"
    FRIDAY = "piątek"
    SATURDAY = "sobota"
    SUNDAY = "niedziela"

    @classmethod
    def choices(cls):
        return tuple((i.name, i.value) for i in cls)

    @classmethod
    def values(cls):
        return [i.value for i in cls]
