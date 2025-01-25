from dataclasses import dataclass, field
from datetime import datetime
import uuid

import pandas as pd


@dataclass
class UserEntity:
    name: str
    age: int
    is_male: bool
    prefecture: str
    city: str
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: datetime = field(default_factory=datetime.now)


class User:
    def __init__(self, driver_user):
        self.user_repository = driver_user

    def get_all_users(self):
        user_rows = self.user_repository.get_all()
        user_df = pd.DataFrame(user_rows, columns=user_rows[0].keys())
        return user_df

    def get_user_by_attrs(
        self, name: str, age: int, sex: str, prefecture: str, city: str
    ) -> UserEntity:
        user_rows = self.user_repository.find_by_attrs(
            name, age, sex == "男性", prefecture, city
        )
        if len(user_rows) == 0:
            return None
        user_row = user_rows[0]
        return UserEntity(**user_row)

    def get_user(self, user_id: int) -> UserEntity:
        user_row = self.user_repository.get(user_id)
        if user_row is None:
            return None
        return UserEntity(
            id=user_id,
            created_at=user_row["created_at"],
            name=user_row["name"],
            age=user_row["age"],
            is_male=user_row["is_male"],
            prefecture=user_row["prefecture"],
            city=user_row["city"]
        )

    def create_user(self, user_id, name: str, age: int, sex: str, prefecture: str, city: str) -> uuid.UUID:
        user = UserEntity(id=user_id, name=name, age=age, is_male=sex == "男性", prefecture=prefecture, city=city)
        self.user_repository.post(user)
        return user.id
