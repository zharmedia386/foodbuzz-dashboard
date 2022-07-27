from pymongo import MongoClient
from datetime import datetime
from bson.objectid import ObjectId

cluster = MongoClient("mongodb+srv://zhar:zhar@cluster0.e99t7.mongodb.net/myFirstDatabase?retryWrites=true&w=majority", tls=True, tlsAllowInvalidCertificates=True)

# Connect to the database
db = cluster["foodbuzz"]

# Connect to the collection
db_users = db["users"]
orders = db["orders"]
items = db["items"]
db_umkm_lists = db["umkm_lists"]

def get_data() :
    # Count numbers of users
    numbers_users = db_users.aggregate([{"$group": {"_id": None, "count": {"$sum": 1}}}])
    # print("Number of users:", next(numbers_users)["count"])
    numbers_users = next(numbers_users)["count"]

    # Count numbers of orders
    numbers_orders = orders.aggregate([{"$group": {"_id": None, "count": {"$sum": 1}}}])
    # print("Number of orders:", next(numbers_orders)["count"])
    numbers_orders = next(numbers_orders)["count"]

    # Count numbers of items
    numbers_items = items.aggregate([{"$group": {"_id": None, "count": {"$sum": 1}}}])
    # print("Number of items:", next(numbers_items)["count"])
    numbers_items = next(numbers_items)["count"]

    # Count status of users
    status_users = db_users.aggregate([{"$group": {"_id": "$status", "count": {"$sum": 1}}}])
    # for status in status_users:
        # print(status["_id"], ":", status["count"])
    

    # Sum total profit of orders
    total_profit = orders.aggregate([{"$group": {"_id": None, "total": {"$sum": "$report.total_profit"}}}])
    # print("Total profit:", next(total_profit)["total"])
    total_profit = next(total_profit)["total"]

    # Count number of item ordered
    item_ordered = orders.aggregate([{"$group": {"_id": None, "total": {"$sum": "$report.total_sell"}}}])
    # print("Total item ordered:", next(item_ordered)["total"])
    item_ordered = next(item_ordered)["total"]

    # Average profit of orders
    # average_profit = orders.aggregate([{"$group": {"_id": None, "total": {"$sum": "$report.average_profit"}}}])
    # print("Average profit:", next(average_profit)["total"])
    # average_profit = next(average_profit)["total"]

    # Select Users
    users_list = db_users.find()
    # for person in users_list:
        # print(person['number'])
    image_users = ['images/faces/face1.jpg', 'images/faces/face2.jpg', 'images/faces/face3.jpg', 'images/faces/face4.jpg']

    # Select UMKM 
    umkm_lists = db_umkm_lists.find()

    return numbers_users, numbers_orders, numbers_items, status_users, total_profit, item_ordered, users_list, image_users, db_users, db_umkm_lists

# test = get_data()