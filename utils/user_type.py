from enum import Enum

class RoleEnum(str, Enum):
    admin = "admin"
    client = "client"
    technician = "technician"

