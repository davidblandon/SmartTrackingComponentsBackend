from pydantic import BaseModel, Field
from datetime import date, datetime

'''
    TEST ATTRIBUTES
    - self.test_id - int - unique identifier of the test
    - self.date - datetime - date of the test
    - self.type - str - type of the test
    - self.technician - str - technician who performed the test
    - self.notes - str - notes about the test
    - self.file - str - file related to the test
'''


class Test(BaseModel):
    date: datetime = None
    type: str
    technician: str
    notes: str = ""
    file = str = ""

    class Config:
        orm_mode = True
    