import os
from typing import Optional, List
from pymongo import MongoClient
from langchain.tools import tool

# MongoDB Connection
CONNECTION_STRING = os.getenv("MONGO_CONNECTION_STRING")
client = MongoClient(CONNECTION_STRING)
db = client["data"]
collection = db["college_cutoffs"]

@tool
def search(
    college: Optional[str] = None,
    program: Optional[str] = None,
    quota: Optional[str] = None,
    category: Optional[str] = None,
    gender: Optional[str] = None,
    min_rank: Optional[int] = None,
    max_rank: Optional[int] = None,
) -> List[dict]:
    """Search MongoDB collection for college cutoffs based on various filters.
       If no college name is provided, return top 5 distinct colleges.
    """

    query = {}

    if college:
        query["Collegename"] = college
    if program:
        query["Program"] = program
    if quota:
        query["Quota"] = quota
    if category:
        query["Category"] = category
    if gender:
        query["Gender"] = gender
    if min_rank is not None and max_rank is not None:
        query["Cutoff"] = {"$gte": min_rank, "$lte": max_rank}
    elif min_rank is not None:
        query["Cutoff"] = {"$gte": min_rank}
    elif max_rank is not None:
        query["Cutoff"] = {"$lte": max_rank}

    # If a college name is provided, return matching records
    if college:
        results = list(collection.find(query))
    
    # If no college name is provided, get top 5 unique colleges
    else:
        pipeline = [
            {"$match": query},  # Apply filters (excluding college name)
            {"$group": {"_id": "$Collegename", "document": {"$first": "$$ROOT"}}},  # Group by Collegename
            {"$replaceRoot": {"newRoot": "$document"}},  # Extract original document
            {"$limit": 5}  # Limit to 5 results
        ]
        results = list(collection.aggregate(pipeline))

    return results[:3] if len(results)>3 else results

# # Run test
# print(search()) Should return top 5 distinct colleges
# print(search(program="Biotechnology and Biochemical Engineering (4 Years, Bachelor of Technology)")) Should return results with this program
# print(search(min_rank=40000)) # Should return IIT Bombay records

