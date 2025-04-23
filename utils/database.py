import os
import sqlalchemy as sa
from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Float, DateTime, Text, Boolean, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base
from sqlalchemy.sql import func
import pandas as pd
from datetime import datetime

# Get the database URL from environment variables
DATABASE_URL = os.getenv("DATABASE_URL")

# Create engine
engine = create_engine(DATABASE_URL)

# Create base class for declarative models
Base = declarative_base()

# Define models
class Project(Base):
    __tablename__ = "projects"
    
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    ip_terms = Column(Text, nullable=True)
    created_at = Column(DateTime, default=func.now())
    transaction_signature = Column(String(100), nullable=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "ip_terms": self.ip_terms,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
            "transaction_signature": self.transaction_signature
        }

class Milestone(Base):
    __tablename__ = "milestones"
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    deadline = Column(DateTime, nullable=True)
    payment_amount = Column(Float, default=0)
    deliverables = Column(Text, nullable=True)
    status = Column(String(50), default="Pending")  # Pending, Funded, Completed, Approved
    created_at = Column(DateTime, default=func.now())
    transaction_signature = Column(String(100), nullable=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "title": self.title,
            "description": self.description,
            "deadline": self.deadline.strftime("%Y-%m-%d") if self.deadline else None,
            "payment_amount": self.payment_amount,
            "deliverables": self.deliverables,
            "status": self.status,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None,
            "transaction_signature": self.transaction_signature
        }

class Participant(Base):
    __tablename__ = "participants"
    
    id = Column(Integer, primary_key=True)
    project_id = Column(Integer, ForeignKey("projects.id"))
    name = Column(String(255), nullable=False)
    role = Column(String(255), nullable=True)
    wallet_address = Column(String(100), nullable=True)
    contribution_percentage = Column(Float, default=0)
    confidential_details = Column(Text, nullable=True)
    joined_at = Column(DateTime, default=func.now())
    transaction_signature = Column(String(100), nullable=True)
    
    def to_dict(self):
        return {
            "id": self.id,
            "project_id": self.project_id,
            "name": self.name,
            "role": self.role,
            "wallet_address": self.wallet_address,
            "contribution_percentage": self.contribution_percentage,
            "confidential_details": self.confidential_details,
            "joined_at": self.joined_at.strftime("%Y-%m-%d %H:%M:%S") if self.joined_at else None,
            "transaction_signature": self.transaction_signature
        }

class Transaction(Base):
    __tablename__ = "transactions"
    
    id = Column(Integer, primary_key=True)
    signature = Column(String(100), nullable=False, unique=True)
    tx_type = Column(String(50), nullable=False)  # create_project, add_milestone, add_participant, etc.
    status = Column(String(50), default="Confirmed")  # Confirmed, Failed
    blocktime = Column(Integer, nullable=True)
    slot = Column(Integer, nullable=True)
    data = Column(Text, nullable=True)  # JSON data 
    created_at = Column(DateTime, default=func.now())
    
    def to_dict(self):
        return {
            "id": self.id,
            "signature": self.signature,
            "tx_type": self.tx_type,
            "status": self.status,
            "blocktime": self.blocktime,
            "slot": self.slot,
            "data": self.data,
            "created_at": self.created_at.strftime("%Y-%m-%d %H:%M:%S") if self.created_at else None
        }

# Create tables if they don't exist
def create_tables():
    Base.metadata.create_all(engine)

# Session maker
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Database connection context manager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Initialize database
def init_db():
    create_tables()
    print("Database tables created")

# CRUD Operations

# Projects
def create_project(name, description, ip_terms=None, transaction_signature=None):
    db = SessionLocal()
    try:
        project = Project(
            name=name,
            description=description,
            ip_terms=ip_terms,
            transaction_signature=transaction_signature
        )
        db.add(project)
        db.commit()
        db.refresh(project)
        return project
    finally:
        db.close()

def get_projects():
    db = SessionLocal()
    try:
        projects = db.query(Project).all()
        return [project.to_dict() for project in projects]
    finally:
        db.close()

def get_project(project_id):
    db = SessionLocal()
    try:
        project = db.query(Project).filter(Project.id == project_id).first()
        return project.to_dict() if project else None
    finally:
        db.close()

# Milestones
def create_milestone(project_id, title, description, deadline=None, payment_amount=0, 
                   deliverables=None, status="Pending", transaction_signature=None):
    db = SessionLocal()
    try:
        milestone = Milestone(
            project_id=project_id,
            title=title,
            description=description,
            deadline=deadline,
            payment_amount=payment_amount,
            deliverables=deliverables,
            status=status,
            transaction_signature=transaction_signature
        )
        db.add(milestone)
        db.commit()
        db.refresh(milestone)
        return milestone
    finally:
        db.close()

def get_milestones(project_id=None):
    db = SessionLocal()
    try:
        query = db.query(Milestone)
        if project_id:
            query = query.filter(Milestone.project_id == project_id)
        milestones = query.all()
        return [milestone.to_dict() for milestone in milestones]
    finally:
        db.close()

def update_milestone_status(milestone_id, status):
    db = SessionLocal()
    try:
        milestone = db.query(Milestone).filter(Milestone.id == milestone_id).first()
        if milestone:
            milestone.status = status
            db.commit()
            db.refresh(milestone)
            return milestone.to_dict()
        return None
    finally:
        db.close()

# Participants
def create_participant(project_id, name, role, wallet_address=None, 
                      contribution_percentage=0, confidential_details=None, 
                      transaction_signature=None):
    db = SessionLocal()
    try:
        participant = Participant(
            project_id=project_id,
            name=name,
            role=role,
            wallet_address=wallet_address,
            contribution_percentage=contribution_percentage,
            confidential_details=confidential_details,
            transaction_signature=transaction_signature
        )
        db.add(participant)
        db.commit()
        db.refresh(participant)
        return participant
    finally:
        db.close()

def get_participants(project_id=None):
    db = SessionLocal()
    try:
        query = db.query(Participant)
        if project_id:
            query = query.filter(Participant.project_id == project_id)
        participants = query.all()
        return [participant.to_dict() for participant in participants]
    finally:
        db.close()

# Transactions
def record_transaction(signature, tx_type, status="Confirmed", blocktime=None, 
                      slot=None, data=None):
    db = SessionLocal()
    try:
        transaction = Transaction(
            signature=signature,
            tx_type=tx_type,
            status=status,
            blocktime=blocktime,
            slot=slot,
            data=data
        )
        db.add(transaction)
        db.commit()
        db.refresh(transaction)
        return transaction
    finally:
        db.close()

def get_recent_transactions(limit=10):
    db = SessionLocal()
    try:
        transactions = db.query(Transaction).order_by(Transaction.created_at.desc()).limit(limit).all()
        return [tx.to_dict() for tx in transactions]
    finally:
        db.close()

def get_transaction(signature):
    db = SessionLocal()
    try:
        transaction = db.query(Transaction).filter(Transaction.signature == signature).first()
        return transaction.to_dict() if transaction else None
    finally:
        db.close()

# Initialize the database when imported
init_db()