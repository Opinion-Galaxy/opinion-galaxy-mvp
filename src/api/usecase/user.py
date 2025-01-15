from dataclasses import dataclass
from datetime import datetime
import uuid


@dataclass
class UserEntity:
    id: uuid.UUID
    created_at: datetime
    name: str
    age: int
    is_male: bool
    address: str
    questionnaire_id: int

    def __init__(self, name: str, age: int, is_male: bool, address: str):
        self.id = uuid.uuid4()
        self.created_at = datetime.now()
        self.name = name
        self.age = age
        self.is_male = is_male
        self.address = address


class User:
    def __init__(self, driver):
        self.user_repository = driver.User()

    def get_all_users(self):
        return self.user_repository.get_all()

    def get_user(self, user_id: int) -> UserEntity:
        return self.user_repository.get(user_id).iloc[0].to_dict()

    def create_user(self, name: str, age: int, sex: str, address: str) -> uuid.UUID:
        user = UserEntity(name=name, age=age, is_male=sex == "男性", address=address)
        self.user_repository.post(user)
        return user.id
