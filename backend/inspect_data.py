import csv
import os


DATA_FOLDER="data"

files=[
    "customers.csv",
    "claims.csv",
    "policies.csv",
    "claim_documents.csv",
    "hospitals.csv",
    "customer_interactions.csv",
    "evaluation_questions.csv"
]

for filename in files:

    filepath=os.path.join(DATA_FOLDER,filename)

    print("\n" + "="*70)
    print(f"FILE:{filename}")
    print("="*70)

    if not os.path.exists(filepath):
        print(" File not found")
        continue

    with open(
        filepath,
        "r",
        encoding="utf-8-sig",
        newline=""
    ) as file:

        reader=csv.reader(file)
        rows=list(reader)

    if not rows:
        print("File is empty")
        continue

    headers=rows[0]

    print(f"\nNumber of columns:", {len(headers)})
    print(f"Number of data rows:", {len(rows)-1})

    print("\nColumns:")

    for index,column in enumerate(headers,start=1):
        print(f"{index}.{column}")

    print("\nFirst 2 rows:")

    for row in rows[1:3]:
        print(row)
