class Count:
    def __init__(self):
        self.count = 0
        self.count_clean = 0

    def increment_count(self):
        self.count += 1
        return self.count
    def increment_count_clean(self):
        self.count_clean += 1
        return self.count_clean