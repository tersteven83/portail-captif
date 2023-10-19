from typing import Optional

from sqlalchemy import Integer, VARCHAR, ForeignKey, Column
from sqlalchemy.orm import Mapped, mapped_column, relationship
from . import db

class Radcheck(db.Model):
    __tablename__ = "radcheck"

    # primary key=True
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(VARCHAR(255), unique=True, index=True)
    attribute: Mapped[str]
    op: Mapped[str]
    value: Mapped[str]
    


class Voucher(db.Model):
    __tablename__ = "voucher"
    
    id: Mapped[int] = mapped_column(primary_key=True)
    voucher_code: Mapped[str] = mapped_column(ForeignKey('radcheck.username'))
    is_active: Mapped[bool] = mapped_column(default=False)
    telephone_number: Mapped[Optional[str]]



# id = Column(Integer, primary_key=True)
#     username = Column(VARCHAR(255), unique=True)
#     attribute = Column(VARCHAR(255))
#     op = Column(VARCHAR(255))
#     value = Column(VARCHAR)
