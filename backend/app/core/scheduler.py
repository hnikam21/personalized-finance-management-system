from apscheduler.schedulers.background import BackgroundScheduler
from sqlalchemy.orm import Session
from app.db.database import SessionLocal
from datetime import datetime


scheduler = BackgroundScheduler()


# ------------------------------
# MONTHLY JOB (Goal Allocation)
# ------------------------------

def monthly_allocation_job():
    print("Running monthly goal allocation...")

    db: Session = SessionLocal()

    try:
        from app.models.user import User
        from app.services.goal_allocation_service import allocate_monthly_savings

        users = db.query(User).all()

        for user in users:
            allocate_monthly_savings(db, user.id)

        print("Monthly allocation completed.")

    except Exception as e:
        print("Monthly job error:", e)

    finally:
        db.close()


# ------------------------------
# DAILY JOB (Alerts)
# ------------------------------

def daily_alert_job():
    print("Running daily alert checks...")

    db: Session = SessionLocal()

    try:
        from app.models.user import User
        from app.services.alert_service import generate_alerts

        users = db.query(User).all()

        for user in users:
            generate_alerts(db, user.id)

        print("Daily alerts processed.")

    except Exception as e:
        print("Daily job error:", e)

    finally:
        db.close()


def start_scheduler():

    # Monthly allocation → 1st of month 00:05
    scheduler.add_job(
        monthly_allocation_job,
        trigger="cron",
        day=1,
        hour=0,
        minute=5
    )
#     scheduler.add_job(
#     monthly_allocation_job,
#     trigger="interval",
#     minutes=1
# )


    # Daily alerts → Every day at 8 AM
    scheduler.add_job(
        daily_alert_job,
        trigger="cron",
        hour=8,
        minute=0
    )
#     scheduler.add_job(
#     daily_alert_job,
#     trigger="interval",
#     minutes=1
# )


    scheduler.start()
