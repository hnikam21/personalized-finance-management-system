from app.db.database import engine, Base

# Import all models so SQLAlchemy registers them
from app.models.user import User
from app.models.income import Income
from app.models.expense import Expense
from app.models.category import Category
from app.models.goal import Goal
from app.models.investment import Investment
from app.models.debt import Debt
from app.models.alert import Alert
from app.models.goal_allocation import GoalAllocation
from app.models.user_training_data import UserTrainingData

def create_tables():
    Base.metadata.create_all(bind=engine)
