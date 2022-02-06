from __future__ import annotations

import uuid
from datetime import datetime


from sqlalchemy import Column, String, DateTime
from sqlalchemy.dialects.postgresql import UUID

from directory.lib.db import Base

from directory.lib.utils import gen_uuid


class Token(Base):
    __tablename__ = "tokens"

    id = Column(UUID, primary_key=True, default=gen_uuid)
    # I know it's not secure :eye-rolling
    token = Column(String, primary_key=False, index=True, unique=True)
    comment = Column(String, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
