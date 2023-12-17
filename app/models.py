from typing import Optional

from sqlalchemy import Integer, VARCHAR, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from . import db
from datetime import datetime
from sqlalchemy_utils import generic_repr

@generic_repr
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
    mac_address: Mapped[str] = mapped_column(VARCHAR(255))
    printed: Mapped[bool] = mapped_column(default=0)
    

@generic_repr
class Radacct(db.Model):
    __tablename__ = "radacct"
    
    radacctid: Mapped[int] = mapped_column(Integer, primary_key=True)
    acctsessionid: Mapped[str] = mapped_column(VARCHAR(64), nullable=False)
    acctuniqueid: Mapped[str] = mapped_column(VARCHAR(32), nullable=False)
    username: Mapped[str] = mapped_column(VARCHAR(64), nullable=False)
    realm: Mapped[str] = mapped_column(VARCHAR(64))
    nasipaddress: Mapped[str] = mapped_column(VARCHAR(15), nullable=False)
    nasportid: Mapped[str] = mapped_column(VARCHAR(32))
    nasporttype: Mapped[str] = mapped_column(VARCHAR(32))
    acctstarttime: Mapped[datetime] = mapped_column(DateTime)
    acctstoptime: Mapped[datetime] = mapped_column(DateTime)
    acctinterval: Mapped[int] = mapped_column(Integer)
    acctsessiontime: Mapped[int] = mapped_column(Integer)
    acctauthentic: Mapped[str] = mapped_column(VARCHAR(32))
    connectinfo_start: Mapped[str] = mapped_column(VARCHAR(50))
    connectinfo_stop: Mapped[str] = mapped_column(VARCHAR(50))
    acctinputoctets: Mapped[int] = mapped_column(Integer)
    acctoutputoctets: Mapped[int] = mapped_column(Integer)
    calledstationid: Mapped[str] = mapped_column(VARCHAR(50), nullable=False)
    callingstationid: Mapped[str] = mapped_column(VARCHAR(50), nullable=False)
    acctterminatecause: Mapped[str] = mapped_column(VARCHAR(32), nullable=False)
    servicetype: Mapped[str] = mapped_column(VARCHAR(32))
    framedprotocol: Mapped[str] = mapped_column(VARCHAR(32))
    framedipaddress: Mapped[str] = mapped_column(VARCHAR(15), nullable=False)
    framedipv6address: Mapped[str] = mapped_column(VARCHAR(45), nullable=False)
    framedipv6prefix: Mapped[str] = mapped_column(VARCHAR(45), nullable=False)
    framedinterfaceid: Mapped[str] = mapped_column(VARCHAR(44), nullable=False)
    delegatedipv6prefix: Mapped[str] = mapped_column(VARCHAR(45), nullable=False)
    

@generic_repr
class Userinfo(db.Model):
    __tablename__ = "userinfo"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    username: Mapped[str] = mapped_column(VARCHAR(128))
    firstname: Mapped[str] = mapped_column(VARCHAR(200))
    lastname: Mapped[str] = mapped_column(VARCHAR(200))
    email: Mapped[str] = mapped_column(VARCHAR(200))
    department: Mapped[str] = mapped_column(VARCHAR(200))
    company: Mapped[str] = mapped_column(VARCHAR(200))
    workphone: Mapped[str] = mapped_column(VARCHAR(200))
    homephone: Mapped[str] = mapped_column(VARCHAR(200))
    address: Mapped[str] = mapped_column(VARCHAR(200))
    city: Mapped[str] = mapped_column(VARCHAR(200))
    state: Mapped[str] = mapped_column(VARCHAR(200))
    country: Mapped[str] = mapped_column(VARCHAR(200))
    zip: Mapped[str] = mapped_column(VARCHAR(200))
    notes: Mapped[str] = mapped_column(VARCHAR(200))
    changeuserinfo: Mapped[str] = mapped_column(VARCHAR(128))
    portalloginpassword: Mapped[str] = mapped_column(VARCHAR(128))
    enableportallogin: Mapped[int] = mapped_column(Integer, insert_default=0)
    creationdate: Mapped[datetime] = mapped_column(DateTime, insert_default=datetime(1, 1, 1, 0, 0, 0))
    creationby: Mapped[str] = mapped_column(VARCHAR(128))
    updatedate: Mapped[datetime] = mapped_column(DateTime, insert_default=datetime(1, 1, 1, 0, 0, 0))
    updateby: Mapped[str] = mapped_column(VARCHAR(128))
    tmp_passcode: Mapped[str] = mapped_column(VARCHAR(6))
    can_be_edited: Mapped[bool] = mapped_column(insert_default=0)
    
class Number_auth(db.Model):
    __tablename__ = "number_auth"
    
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    code: Mapped[str] = mapped_column(VARCHAR(255), unique=True, index=True)
    expiration: Mapped[datetime] = mapped_column(DateTime)
    already_ask_voucher: Mapped[bool] = mapped_column(insert_default=0)
    