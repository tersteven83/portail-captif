from typing import Optional

from sqlalchemy import Integer, VARCHAR, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from . import db
from datetime import datetime

class Radcheck(db.Model):
    __tablename__ = "radcheck"

    # primary key=True
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(VARCHAR(255), unique=True, index=True)
    attribute: Mapped[str] = mapped_column(VARCHAR(255))
    op: Mapped[str] = mapped_column(VARCHAR(255))
    value: Mapped[str] = mapped_column(VARCHAR(255))
    


class Voucher(db.Model):
    __tablename__ = "voucher"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    voucher_code: Mapped[str] = mapped_column(ForeignKey('radcheck.username', ondelete="CASCADE", onupdate="CASCADE"))
    is_active: Mapped[bool] = mapped_column(default=0)
    telephone_number: Mapped[Optional[str]] = mapped_column(VARCHAR(255))
    date: Mapped[datetime] = mapped_column(DateTime)

