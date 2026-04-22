class Notifier:
    """Real notifier — replaced by Mock in tests"""
    def notify(self, message: str):
        print(f"[NOTIFY] {message}")