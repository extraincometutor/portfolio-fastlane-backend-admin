from bson import ObjectId
from datetime import datetime

def fix_id(obj):
    if isinstance(obj, list):
        for item in obj:
            fix_id(item)
    elif isinstance(obj, dict):
        if "_id" in obj:
            obj["id"] = str(obj["_id"])
        for key, value in obj.items():
            if isinstance(value, (dict, list, ObjectId, datetime)):
                if isinstance(value, ObjectId):
                    obj[key] = str(value)
                elif isinstance(value, datetime):
                    obj[key] = value.isoformat()
                else:
                    fix_id(value)
    return obj
