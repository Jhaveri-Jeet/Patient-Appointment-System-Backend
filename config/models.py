from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from config.database import Base


class Admin(Base):
    __tablename__ = "Admin"

    Id = Column(Integer, primary_key=True)
    Username = Column(String(255), nullable=False)
    HashPassword = Column(String(255), nullable=False)


class Patient(Base):
    __tablename__ = "Patients"

    Id = Column(Integer, primary_key=True)
    Name = Column(String(255), nullable=False)
    Mobile = Column(String(255), nullable=False)
    Email = Column(String(255), unique=True, nullable=False)
    Password = Column(String(255), nullable=False)
    Address = Column(String(255), nullable=False)
    Gender = Column(String(255), nullable=False)

    appointments = relationship("Appointment", back_populates="patient")


class Appointment(Base):
    __tablename__ = "Appointments"

    Id = Column(Integer, primary_key=True)
    Problem = Column(String(255), nullable=False)
    Date = Column(Date, nullable=False)
    PatientId = Column(Integer, ForeignKey("Patients.Id"), nullable=False)

    patient = relationship("Patient", back_populates="appointments")
