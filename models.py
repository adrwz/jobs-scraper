"""
Models & enums
"""

from enum import Enum, unique


class StringEnum(str, Enum):
    """
    Enums that auto convert to strings
    """

    def __str__(self):
        return str(self.value)

    def __repr__(self):
        return str(self.value)


@unique
class ATSBaseURL(StringEnum):
    """
    This class represents the base URLs for different ATS platforms
    """

    GREENHOUSE = "boards.greenhouse.io"
    WELLFOUND = "wellfound.com"
    LEVER = "jobs.lever.co"
    ASHBY = "jobs.ashby.com"
    WORKABLE = "apply.workable.com"
