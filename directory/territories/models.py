from __future__ import annotations

from sqlalchemy import Column, Integer, String, Enum, ForeignKey
from sqlalchemy.orm import relationship

from directory.lib.db import Base
from directory.territories.enums import KATOTTGCategory, KOATUUCategory


class KATOTTG(Base):
    __tablename__ = "katottg"

    code = Column(String, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    name_en = Column(String, nullable=False)
    level = Column(Integer, index=True, nullable=False)
    parent_id = Column(String, ForeignKey(code), index=True, nullable=True)
    category = Column(Enum(KATOTTGCategory), index=True, nullable=False)
    children_count = Column(Integer, default=0, nullable=False)

    parent = relationship("KATOTTG", remote_side=[code])

    def __str__(self):
        return f"{self.code} - {self.name}"


class KOATUU(Base):
    __tablename__ = "koatuu"

    code = Column(String, primary_key=True, index=True)
    category = Column(Enum(KOATUUCategory), index=True, nullable=True)
    name = Column(String, index=True, nullable=False)
    name_en = Column(String, nullable=False)
    katottg_code = Column(String, index=True, nullable=True)
    katottg_name = Column(String, index=True, nullable=True)
    katottg_category = Column(Enum(KATOTTGCategory), index=True, nullable=True)

    def __str__(self):
        return f"{self.code} - {self.name}"
