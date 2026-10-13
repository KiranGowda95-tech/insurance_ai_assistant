
from sqlalchemy import select, func
from database.connection import SessionLocal
from database.models import CustomerInteraction


def get_interaction_analytics():
    db = SessionLocal()

    try:
        total_interactions = (
            db.execute(
                select(func.count(CustomerInteraction.interaction_id))
            ).scalar_one()
        )

        unique_customers = (
            db.execute(
                select(
                    func.count(
                        func.distinct(CustomerInteraction.customer_id)
                    )
                )
            ).scalar_one()
        )

        def get_breakdown(column):
            rows = db.execute(
                select(
                    column,
                    func.count(CustomerInteraction.interaction_id)
                )
                .group_by(column)
                .order_by(
                    func.count(CustomerInteraction.interaction_id).desc()
                )
            ).all()

            return [
                {
                    "category": category if category is not None else "Unknown",
                    "count": count
                }
                for category, count in rows
            ]

        return {
            "total_interactions": total_interactions,
            "unique_customers": unique_customers,
            "by_channel": get_breakdown(CustomerInteraction.channel),
            "by_intent": get_breakdown(CustomerInteraction.intent),
            "by_sentiment": get_breakdown(CustomerInteraction.sentiment),
            "by_resolution_status": get_breakdown(
                CustomerInteraction.resolution_status
            ),
        }

    finally:
        db.close()
