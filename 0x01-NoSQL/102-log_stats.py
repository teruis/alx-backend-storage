#!/usr/bin/env python3
""" 102-log_stats """
from pymongo import MongoClient

def log_stats(mongo_collection):
    total_logs = mongo_collection.count_documents({})
    print(f"{total_logs} logs")

    # Aggregation pipeline to count the occurrence of each IP
    pipeline = [
        {"$group": {"_id": "$ip", "count": {"$sum": 1}}},
        {"$sort": {"count": -1}},
        {"$limit": 10}  # Limit to the top 10 IPs
    ]

    top_ips = list(mongo_collection.aggregate(pipeline))

    print("IPs:")
    for ip_data in top_ips:
        ip = ip_data["_id"]
        count = ip_data["count"]
        print(f"    {ip}: {count}")

if __name__ == "__main__":
    client = MongoClient('mongodb://127.0.0.1:27017')
    logs_collection = client.logs_database.nginx  # Assuming nginx collection is in logs_database
    log_stats(logs_collection)
