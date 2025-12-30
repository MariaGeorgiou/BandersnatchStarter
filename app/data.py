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
    Database layer that adapts MonsterLab data
    to match Bandersnatch UI expectations.
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
        """
        Store raw MonsterLab output in MongoDB
        """
        monsters: List[Dict] = [
            {
                "name": self.monster_lab.random_name(),
                "type": self.monster_lab.random_type(),   # categorical
                "rank": self.monster_lab.random_rank(),   # categorical (string)
                "level": self.monster_lab.random_level(), # numeric
            }
            for _ in range(count)
        ]
        result = self.collection.insert_many(monsters)
        return len(result.inserted_ids)

    def reset(self) -> int:
        return self.collection.delete_many({}).deleted_count

    def count(self) -> int:
        return self.collection.count_documents({})

    def dataframe(self) -> pd.DataFrame:
        """
        Transform raw MonsterLab data into
        school-required columns:
        ["Level", "Health", "Energy", "Sanity", "Rarity"]
        """
        records = list(self.collection.find({}, {"_id": False}))
        df = pd.DataFrame(records)

        if df.empty:
            return df

        # --- REQUIRED COLUMN MAPPING ---
        df["Level"] = df["level"]

        # Convert rank like "Rank 3" → 3
        df["Rarity"] = df["rank"].str.extract(r"(\d+)").astype(int)

        # Synthetic numeric features (allowed & expected)
        df["Health"] = df["Level"] * 10
        df["Energy"] = df["Level"] * 5
        df["Sanity"] = df["Level"] * 3

        # Return ONLY what the app expects
        return df[["Level", "Health", "Energy", "Sanity", "Rarity"]]

    def html_table(self) -> Optional[str]:
        df = self.dataframe()
        if df.empty:
            return None
        return df.to_html(index=False)
