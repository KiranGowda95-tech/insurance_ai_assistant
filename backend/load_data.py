import csv 
from datetime import datetime

from sqlalchemy import insert

from database.connection import SessionLocal

from database.models import (
    Customer,
    Policy,
    Claim,
    ClaimDocument,
    Hospital,
    CustomerInteraction,
)

DATA_FOLDER="data"

BATCH_SIZE=5000

def parse_date(value):

    if not value:
        return None

    return datetime.strptime(
        value,
        "%Y-%m-%d"
    ).date()

def parse_float(value):

    if value is None or value == "":
        return None

    return float(value)

def parse_int(value):

    if value is None or value=="":
        return None
    return int(value)

def parse_bool(value):

    if value is None or value=="":
        return None
    return value.strip() in ["1","true","True","TRUE"]

def load_csv(filename,model,transform_function):
    

    filepath=f"{DATA_FOLDER}/{filename}"

    print()
    print("="*60)
    print(f"Loading {filename}")
    print("="*60)

    db=SessionLocal()

    total=0
    batch=[]

    try:

        with open(
            filepath,
            "r",
            encoding="utf-8-sig",
            newline=""
        ) as file:
            reader = csv.DictReader(file)

            for row in reader:
                data=transform_function(row)
                batch.append(data)

                if len(batch) >=BATCH_SIZE:

                    db.execute(
                        insert(model),
                        batch
                    )

                    db.commit()

                    total += len(batch)

                    print(f"Inserted{total:,} rows...")

                    batch.clear()
            if batch:

                db.execute(
                    insert(model),
                    batch
                )

                db.commit()

                total +=len(batch)

            print(
                f"Finished {filename}:{total:,} rows"
            )

    except Exception as error:

        db.rollback()

        print(f"Error loading {filename}:")

        print(error)

        raise
    finally:
        db.close()



    # CUSTOMERS

def transform_customer(row):

    return {
        "customer_id": row["customer_id"],
        "customer_name": row["customer_name"],
        "age": parse_int(row["age"]),
        "gender": row["gender"],
        "city":row["city"],
        "state":row["state"],
        "customer_since":parse_date(
            row["customer_since"]
        ),
        "kyc_status":row["kyc_status"],
        "risk_segment":row["risk_segment"]

    }


def transform_policy(row):
    return {
        "policy_id":row["policy_id"],
        "customer_id":row["customer_id"],
        "policy_type":row["policy_type"],
        "product_name":row["product_name"],
        "policy_start_date":parse_date(
            row["policy_start_date"]
        ),
        "policy_end_date":parse_date(
            row["policy_end_date"]
        ),
        "sum_insured":parse_float(row["sum_insured"]),
        "annual_premium":parse_float(row["annual_premium"]),
        "policy_status":row["policy_status"],
        "co_pay_pct":parse_float(
            row["co_pay_pct"]
        ),
        "deductible":parse_float(
            row["deductible"]
        ),
        "waiting_period_days":parse_int(
            row["waiting_period_days"]
        )
    }

def transform_claim(row):
    return {
        "claim_id":row["claim_id"],
        "customer_id":row["customer_id"],
        "policy_id":row["policy_id"],
        "policy_type":row["policy_type"],
        "claim_date":parse_date(
            row["claim_date"]
        ),
        "claim_amount":parse_float(
            row["claim_amount"]
        ),
        "claim_status":row["claim_status"],
        "approved_amount":parse_float(
            row["approved_amount"]
        ),
        "diagnosis_or_loss_type":
            row["diagnosis_or_loss_type"]
        ,
        "hospital_id":row["hospital_id"] or None,
        "fraud_risk_score":parse_float(
            row["fraud_risk_score"]
        ),
        "manual_review_flag":parse_bool(
            row["manual_review_flag"]
        ),
        "rejection_or_adjustment_reason":
        row["rejection_or_adjustment_reason"] or None
    }

        # CLAIM DOCUMENTS

def transform_claim_document(row):
    return {
        "claim_id":row["claim_id"],
        "document_type":row["document_type"],
        "upload_status":row["upload_status"],
        "verification_status":row["verification_status"],
        "file_type":row["file_type"],
    }

    #HOSPITALS


def transform_hospital(row):
    return {
        "hospital_id":row["hospital_id"],
        "hospital_name":row["hospital_name"],
        "city":row["city"],
        "network_status":row["network_status"],
        "specialty": row["specialty"],
    }

    #CUSTOMER INTERATIONS

def transform_interaction(row):
    return {
        "interaction_id":row["interaction_id"],
        "customer_id":row["customer_id"],
        "claim_id":row["claim_id"] or None,
        "interaction_date":parse_date(row["interaction_date"]),
        "channel":row["channel"],
        "intent":row["intent"],
        "sentiment":row["sentiment"],
        "resolution_status":row["resolution_status"],
    }


if __name__=="__main__":

    load_csv(
        "customers.csv",
        Customer,
        transform_customer
    )

    load_csv(
        "policies.csv",
        Policy,
        transform_policy
    )

    load_csv(
        "claims.csv",
        Claim,
        transform_claim
    )
    load_csv(
        "claim_documents.csv",
        ClaimDocument,
        transform_claim_document
    )
    load_csv(
        "hospitals.csv",
        Hospital,
        transform_hospital
    )
    load_csv(
        "customer_interactions.csv",
        CustomerInteraction,
        transform_interaction
    )


    print()
    print("="*60)
    print(" All Data Loaded Successfully")
    print("="*60)

