from os import getenv
from typing import List, Dict, Optional

import pandas as pd
from pymongo import MongoClient
from dotenv import load_dotenv
from certifi import where
from BloomtechMonsterLab import MonsterLab

load_dotenv()

class Database:
    """
    Local testing version — pre-Flask.
    """

    client = MongoClient(
        getenv("DB_URL"), 
        tlsCAFile=where()
    )
    database = client["MonsterDatabase"]

    def __init__(self, collection_name: str = "monsters"):
        self.collection = self.database[collection_name]
        self.monster_lab = MonsterLab()

    def seed(self, count: int) -> int:
        monsters: List[Dict] = [
            {
                "name": self.monster_lab.random_name(),
                "type": self.monster_lab.random_type(),
                "rank": self.monster_lab.random_rank(),
                "level": self.monster_lab.random_level(),
            }
            for _ in range(count)
        ]
        result = self.collection.insert_many(monsters)
        return len(result.inserted_ids)

    def reset(self) -> int:
        result = self.collection.delete_many({})
        return result.deleted_count

    def count(self) -> int:
        return self.collection.count_documents({})

    def dataframe(self) -> pd.DataFrame:
        records = list(self.collection.find({}, {"_id": False}))
        return pd.DataFrame(records)

    def html_table(self) -> Optional[str]:
        df = self.dataframe()
        if df.empty:
            return None
        return df.to_html(index=False)
