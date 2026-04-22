class Database:
    """Real database — replaced by Mock in tests"""
    def save(self, data: dict):
        print(f"[DB] Saved: {data}")

    def get_history(self, owner: str):
        print(f"[DB] History for {owner}")
        return []