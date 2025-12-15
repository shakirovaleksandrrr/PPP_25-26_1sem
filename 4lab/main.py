import json


class CurrencyRates:
    base_currency = "RUB"
    rates = {}

    @classmethod
    def set_base(cls, base: str):
        cls.base_currency = base

    @classmethod
    def add_rate(cls, currency: str, rate: float):
        cls.rates[currency] = rate

    @classmethod
    def to_base(cls, amount: float, currency: str) -> float:
        if currency == cls.base_currency:
            return amount
        if currency not in cls.rates:
            raise ValueError(f"Неизвестная валюта: {currency}")
        return amount * cls.rates[currency]


class Money:
    # Общий интерфейс: методы to_base() и describe()
    def __init__(self, amount, currency):
        self.amount = amount
        self.currency = currency

    def to_base(self):
        return CurrencyRates.to_base(self.amount, self.currency)

    def describe(self):
        base = self.to_base()
        if self.currency == CurrencyRates.base_currency:
            return f"{self.amount:.2f} {self.currency}"
        return f"{self.amount:.2f} {self.currency} = {base:.2f} {CurrencyRates.base_currency}"


class CodeMoney(Money):
    def __init__(self, amount, currency):
        super().__init__(amount, currency)


class JsonMoney(Money):
    def __init__(self, json_str):
        data = json.loads(json_str)
        super().__init__(float(data["amount"]), data["currency"])


class LocalMoney(Money):
    def __init__(self, raw):
        value = raw.replace("₽", "").replace(" ", "").replace(",", ".")
        super().__init__(float(value), CurrencyRates.base_currency)


class DefaultMoney(Money):
    def __init__(self, amount):
        super().__init__(amount, CurrencyRates.base_currency)


class MoneyCollection:
    def __init__(self):
        self.items = []

    def add(self, money):
        self.items.append(money)

    def total(self):
        return sum(m.to_base() for m in self.items)

    def max(self):
        return max(self.items, key=lambda m: m.to_base())

    def min(self):
        return min(self.items, key=lambda m: m.to_base())

    def list_all(self):
        return [m.describe() for m in self.items]


if __name__ == "__main__":
    CurrencyRates.set_base("RUB")
    CurrencyRates.add_rate("USD", 92.5)
    CurrencyRates.add_rate("EUR", 100.0)
    CurrencyRates.add_rate("CNY", 12.3)

    collection = MoneyCollection()

    inputs = [
        "code 1000 RUB",
        "code 15.5 USD",
        'json {"amount": 200, "currency": "EUR"}',
        "local 1 000,50 ₽",
        "default 500",
        # "code 50 ABC"
    ]

    for s in inputs:
        try:
            if s.startswith("json"):
                collection.add(JsonMoney(s[5:]))
            elif s.startswith("code"):
                _, amount, currency = s.split()
                collection.add(CodeMoney(float(amount), currency))
            elif s.startswith("local"):
                collection.add(LocalMoney(s))
            elif s.startswith("default"):
                _, amount = s.split()
                collection.add(DefaultMoney(float(amount)))
            else:
                print(f"Неизвестный формат: {s}")
        except Exception as e:
            print(f"Ошибка при обработке '{s}': {e}")

    print(f"Total: {collection.total():.2f} RUB")
    print("Max:", collection.max().describe())
    print("Min:", collection.min().describe())
    for line in collection.list_all():
        print(line)
