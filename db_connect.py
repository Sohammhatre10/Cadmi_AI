import pandas as pd
import json
from pymongo import MongoClient
import dotenv
import os

dotenv.load_dotenv()
CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")
client = MongoClient(CONNECTION_STRING)

db = client["data"]
collection = db["college_cutoffs"]
csv_files = ["csab.csv", "iitmain.csv"]
for csv in csv_files:
    df = pd.read_csv(csv)
    json_data = json.loads(df.to_json(orient="records"))
    collection.insert_many(json_data)
    print("Data inserted successfully!")
