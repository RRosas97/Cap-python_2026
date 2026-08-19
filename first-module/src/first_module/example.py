def suma(a, b):
    resultado = a + b
    return resultado


class miClase:
    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

    def saludar(self):
        print("Hola, soy " + self.nombre)


lista_de_numeros_muy_larga_para_forzar_el_limite_de_linea = [
    1,
    2,
    3,
    4,
    5,
    6,
    7,
    8,
    9,
    10,
    11,
    12,
    13,
    14,
    15,
]


def funcion_no_usada():
    return None


if __name__ == "__main__":
    r = suma(1, 2)
    print(r)
