from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base


class Admin(Base):
    __tablename__ = "Admin"

    Id = Column(Integer, primary_key=True)
    Username = Column(String(255), nullable=False)
    HashPassword = Column(String(255), nullable=False)
    FullName = Column(String(255), nullable=True)
    Email = Column(String(255), nullable=True)
    Address = Column(String(255), nullable=True)
    Degree = Column(String(255), nullable=True)


class Patient(Base):
    __tablename__ = "Patients"

    Id = Column(Integer, primary_key=True)
    Name = Column(String(255), nullable=False)
    Mobile = Column(String(255), nullable=False)
    Email = Column(String(255), unique=True, nullable=False)
    Address = Column(String(255), nullable=False)
    Gender = Column(String(255), nullable=False)
    BloodGroup = Column(String(255), nullable=False)

    appointments = relationship("Appointment", back_populates="patient")


class Service(Base):
    __tablename__ = "Services"

    Id = Column(Integer, primary_key=True)
    Name = Column(String(255), nullable=False)
    Description = Column(String(255), nullable=False)
    Price = Column(Integer, nullable=False)

    appointments = relationship("Appointment", back_populates="service")


class Slot(Base):
    __tablename__ = "Slots"

    Id = Column(Integer, primary_key=True)
    Time = Column(String(255), nullable=False)
    Status = Column(String(255), nullable=False, default="Available")

    appointments = relationship("Appointment", back_populates="slot")


class Appointment(Base):
    __tablename__ = "Appointments"

    Id = Column(Integer, primary_key=True)
    Problem = Column(String(255), nullable=False)
    Date = Column(Date, nullable=False)
    Prescription = Column(String(255), default=None)
    Status = Column(String(255), default="Pending")
    PatientId = Column(Integer, ForeignKey("Patients.Id"), nullable=False)
    ServiceId = Column(Integer, ForeignKey("Services.Id"), nullable=False)
    SlotId = Column(Integer, ForeignKey("Slots.Id"), nullable=False)

    patient = relationship("Patient", back_populates="appointments")
    service = relationship("Service", back_populates="appointments")
    slot = relationship("Slot", back_populates="appointments")
