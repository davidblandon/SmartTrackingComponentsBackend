# scripts/create_admin.py
from app.database.collections import user_collection
from app.utils.user_security import hash_password

admin = {
    "name": "Admin Dev",
    "email": "admin@example.com",
    "role": "admin",
    "telephone": "000000000",
    "hashed_password": hash_password("supersecurepassword")
}

res = user_collection.insert_one(admin)
print("Inserted admin id:", res.inserted_id)
