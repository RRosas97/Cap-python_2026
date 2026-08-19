class Animal:
    def __init__(self, especie, edad):
        self.especie = especie
        self.edad = edad

    def hablar(self):
        pass

    def moverse(self):
        pass

    def describeme(self):
        print("Soy un animal del tipo", type(self).__name__)


class Perro(Animal):
    def __init__(self, especie, edad, dueño):
        super().__init__(especie, edad)
        self.dueño = dueño

    def hablar(self):
        print("Guau!")

    def moverse(self):
        print("Caminando con 4 patas")


mi_perro = Perro("mamífero", 10)
