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


class Employee:
    def __init__(self, name: str, salary: float) -> None:
        self.name = name
        self.salary = salary

    def get_name(self) -> str:
        return self.name

    def get_salary(self) -> float:
        return self.salary

    def set_salary(self, new_salary: float) -> None:
        self.salary = new_salary

    def bonus(self, performance_multiplier: float) -> float:
        return self.salary * performance_multiplier

emp = Employee("Alice", 50000)

#emp.set_salary(55000)
#print(emp.get_name())  # Output: Alice
#print(emp.get_salary())  # Output: 55000.0

bonus = emp.bonus(1.1)

print(f"Bonus for {emp.get_name()}: {bonus}")


