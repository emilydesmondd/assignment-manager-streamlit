class Counter:
    def __init__(self, start: int = 0) -> None:
        self.value = start

    def increment(self) -> None:
        self.value += 1

    def current_value(self) -> int:
        return self.value
    
    def increment_by(self, amount: int) -> None:
        self.value += 2

c = Counter(start=5)
c1 = Counter(start=10)
c1.increment()

print(c.current_value())  # Output: 5
print(c1.current_value())  # Output: 11