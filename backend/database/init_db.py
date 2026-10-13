from .connection import engine,Base
from .models import (
    Customer,
    Policy,
    Claim,
    ClaimDocument,
    Hospital,
    CustomerInteraction
)

def initialize_database():
    Base.metadata.create_all(bind=engine)
    print("Insurance database initialized successfully.")



if __name__=="__main__":
    initialize_database()