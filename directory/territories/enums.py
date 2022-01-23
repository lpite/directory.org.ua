from __future__ import annotations
import enum
from functools import lru_cache

from directory.lib.constants import (
    CATEGORY_LATIN_NORMALIZATION_MAP,
    CATEGORY_CYRILLIC_NORMALIZATION_MAP,
)


@enum.unique
class KATOTTGCategory(enum.Enum):
    """
    Тип території
     - O - Область або АРК
     - K - Місто, що має спеціальний статус
     - P - Район в області або в АРК
     - H - Територіальна громада
     - M - Місто
     - T - Селище міського типу
     - C - Село
     - X - Селище
     - B - Район в місті
    """
    region = "O"
    special = "K"
    district = "P"
    community = "H"
    city = "M"
    urban_village = "T"
    village = "C"
    small_village = "X"
    municipal_district = "B"

    @staticmethod
    @lru_cache
    def get_name_mapping() -> dict[KATOTTGCategory, str]:
        return {
            KATOTTGCategory.region: "Область або АРК",
            KATOTTGCategory.special: "Місто, що має спеціальний статус",
            KATOTTGCategory.district: "Район в області або в АРК",
            KATOTTGCategory.community: "Територіальна громада",
            KATOTTGCategory.city: "Місто",
            KATOTTGCategory.urban_village: "Селище міського типу",
            KATOTTGCategory.village: "Село",
            KATOTTGCategory.small_village: "Селище",
            KATOTTGCategory.municipal_district: "Район в місті",
        }

    @property
    def display_name(self) -> str:
        mapping = KATOTTGCategory.get_name_mapping()
        return mapping[self]

    @staticmethod
    def from_value(value: str) -> KATOTTGCategory:

        # convert cyrillic character to latin character
        if value in CATEGORY_LATIN_NORMALIZATION_MAP:
            value = CATEGORY_LATIN_NORMALIZATION_MAP[value]

        return KATOTTGCategory(value)


@enum.unique
class KOATUUCategory(enum.Enum):
    village = "С"  # село
    small_village = "Щ"  # селище
    urban_village = "Т"  # селище міського типу
    city = "М"  # місто
    municipal_district = "Р"  # район міста

    @staticmethod
    def from_value(value: str) -> KOATUUCategory:

        # convert latin character to cyrillic character
        if value in CATEGORY_CYRILLIC_NORMALIZATION_MAP:
            value = CATEGORY_CYRILLIC_NORMALIZATION_MAP[value]

        return KOATUUCategory(value)
