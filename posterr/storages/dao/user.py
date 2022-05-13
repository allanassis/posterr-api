from bson.objectid import ObjectId

from posterr.services.user import User
from posterr.storages.database import DataBase

class UserDao(object):
    
    @staticmethod
    def get(id: str, db: DataBase) -> User:
        user_list = db.client["user"].aggregate([
            { "$match": { "_id": ObjectId(id) } },
            { "$lookup":
                {
                "from": "user",
                "localField": "followers.list",
                "foreignField": "_id",
                "as": "followers",
                }
            },
            { "$lookup":
                {
                "from": "user",
                "localField": "following.list",
                "foreignField": "_id",
                "as": "following"
                }
            },
            { "$lookup":
                {
                "from": "post",
                "localField": "_id",
                "foreignField": "user_id",
                "as": "posts"
                }
            }
        ])
        user = list(user_list).pop()
        return user