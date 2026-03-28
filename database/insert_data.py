from sqlalchemy.orm import sessionmaker
from database.connection import engine
from database.models import Business, Platform, AudienceSegment

SessionLocal = sessionmaker(bind=engine)

def insert_seed_data():
    session = SessionLocal()

    business_exists = session.query(Business).filter(Business.name == "GlowSkin Studio").first()
    if not business_exists:
        session.add(
            Business(
                name="GlowSkin Studio",
                category="Beauty",
                stage="0-500 transactions"
            )
        )

    platform_data = [
        {"name": "TikTok", "type": "social"},
        {"name": "Instagram", "type": "social"},
        {"name": "Reddit", "type": "community"}
    ]
    
    audience_data = [
    {"name": "Gen Z Skincare Enthusiasts", "age_group": "18-24", "interest": "Skincare"},
    {"name": "Working Professionals Fitness", "age_group": "25-34", "interest": "Fitness"},
    {"name": "Budget Conscious Shoppers", "age_group": "18-30", "interest": "Deals"}
    ]

    for item in platform_data:
        exists = session.query(Platform).filter(Platform.name == item["name"]).first()
        if not exists:
            session.add(
                Platform(
                    name=item["name"],
                    type=item["type"]
                )
            )
            
    
    for item in audience_data:
        exists = session.query(AudienceSegment).filter(AudienceSegment.name == item["name"]).first()
        if not exists:
            session.add(
                AudienceSegment(
                    name=item["name"],
                    age_group=item["age_group"],
                    interest=item["interest"]
                )
            )

    session.commit()
    session.close()

    print("Seed data inserted successfully")

if __name__ == "__main__":
    insert_seed_data()