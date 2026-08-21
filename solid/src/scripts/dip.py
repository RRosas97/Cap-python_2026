from abc import ABC, abstractmethod


# FrontEnd depende de la abstracción del data source para mostrar información
# Si dependiera directamente de Database o de la API, si alguna de estas dos
# sufriera un cambio, FrontEnd también tendría que ser modificado. Por eso
# la abstracción Data Source hereda a ambos medios de información el
# método get_data(), que puede ser modificado si así se requiere sin
# interferir con la clase FrontEnd.
class FrontEnd:
    def __init__(self, data_source):
        self.data_source = data_source

    def display_data(self):
        data = self.data_source.get_data()
        print("Display data:", data)


class DataSource(ABC):
    @abstractmethod
    def get_data(self):
        pass


class Database(DataSource):
    def get_data(self):
        return "Data from the database"


class API(DataSource):
    def get_data(self):
        return "Data from the API"
