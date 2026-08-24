from abc import ABC, abstractmethod


# Clases abstractas de las instancias que van a devolver los factories
class Coin(ABC):
    @abstractmethod
    def createCoin(self) -> "Coin":
        pass


class Bill(ABC):
    @abstractmethod
    def createBill(self) -> "Bill":
        pass


class AbstractFactory(ABC):
    @abstractmethod
    def createCoin(self) -> Coin:
        pass

    @abstractmethod
    def createBill(self) -> Bill:
        pass


# Factories de las clases concretas
class MexicanMoneyFactory(AbstractFactory):
    def createCoin(self) -> Coin:
        return MexicanCoin()

    def createBill(self) -> Bill:
        return MexicanBill()


class GermanMoneyFactory(AbstractFactory):
    def createCoin(self) -> Coin:
        return GermanCoin()

    def createBill(self) -> Bill:
        return GermanBill()


# Clases concretas
class MexicanCoin(Coin):
    def createCoin(self):
        return "Moneda: peso"


class MexicanBill(Bill):
    def createBill(self):
        return "Denominaciones de billetes: 20, 50, 100, 500"


class GermanCoin(Coin):
    def createCoin(self):
        return "Moneda: Euro"


class GermanBill(Bill):
    def createBill(self):
        return "Denominaciones: 5, 10, 20, 100"


def make_mexican_money(factory: AbstractFactory):
    moneda = factory.createCoin()
    billete = factory.createBill()
    return moneda.createCoin(), billete.createBill()


money_Factory = MexicanMoneyFactory()

mexican_money = make_mexican_money(money_Factory)

print(mexican_money)
