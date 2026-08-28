from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    database_url:str = (
                "mssql+pyodbc://sa:abcd123@Hijo_del_Trueno/Users?driver=ODBC+Driver+17+for+SQL+Server"
    )
    secret_key: str ="123456"
    algorithm: str ="HS256"
    expiracion_minutos: int = 120

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
