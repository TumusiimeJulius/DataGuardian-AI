from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    DateTime,
    Text,
    ForeignKey
)

from datetime import datetime

from database import Base





class DatasetHistory(Base):

    __tablename__ = "dataset_history"



    # ==============================
    # Dataset ID
    # ==============================

    id = Column(

        Integer,

        primary_key=True,

        index=True

    )





    # ==============================
    # Dataset Information
    # ==============================


    filename = Column(

        String(255),

        nullable=False

    )



    original_file = Column(

        String(255),

        nullable=True

    )



    clean_file = Column(

        String(255),

        nullable=True

    )





    # ==============================
    # AI Data Quality Metrics
    # ==============================


    quality_score = Column(

        Float,

        default=0

    )



    missing_values = Column(

        Integer,

        default=0

    )



    duplicates = Column(

        Integer,

        default=0

    )



    anomalies = Column(

        Integer,

        default=0

    )





    # ==============================
    # AI Generated Insights
    # ==============================


    recommendations = Column(

        Text,

        nullable=True

    )



    root_cause = Column(

        Text,

        nullable=True

    )



    repair_summary = Column(

        Text,

        nullable=True

    )





    # ==============================
    # Pipeline Information
    # ==============================


    status = Column(

        String(50),

        default="COMPLETED"

    )



    execution_time = Column(

        Float,

        default=0

    )



    agents_completed = Column(

        Integer,

        default=0

    )





    # ==============================
    # Timestamp
    # ==============================


    uploaded_at = Column(

        DateTime,

        default=datetime.utcnow

    )





    def __repr__(self):

        return (

            f"<DatasetHistory "

            f"id={self.id} "

            f"filename={self.filename}>"

        )


# ========================================
# User Authentication Models
# ========================================

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=True) # Nullable for Google login accounts
    google_id = Column(String(255), unique=True, index=True, nullable=True)
    profile_picture = Column(String(500), nullable=True)
    reset_code = Column(String(50), nullable=True)
    reset_code_expires_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<User id={self.id} email={self.email}>"


class UserSession(Base):
    __tablename__ = "user_sessions"

    id = Column(String(255), primary_key=True, index=True) # Random UUID token
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    expires_at = Column(DateTime, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<UserSession id={self.id[:8]}... user_id={self.user_id}>"