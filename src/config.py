import dataclasses
from os import environ
import tomllib
import typing



@dataclasses.dataclass
class Config:
    DATABASE_DEV_IP: str
    DATABASE_DEV_NAME: str
    DATABASE_DEV_PASSWORD: str
    DATABASE_DEV_PORT: str
    DATABASE_DEV_USER: str
    DATABASE_PROD_IP: str
    DATABASE_PROD_NAME: str
    DATABASE_PROD_PASSWORD: str
    DATABASE_PROD_PORT: str
    DATABASE_PROD_USER: str
    DATABASE_TEST_IP: str
    DATABASE_TEST_NAME: str
    DATABASE_TEST_PASSWORD: str
    DATABASE_TEST_PORT: str
    DATABASE_TEST_USER: str
    FLASK_APP: str
    FLASK_DEBUG: bool
    FLASK_ENV: str
    GS_AUTH_PROVIDER: str
    GS_AUTH_URI: str
    GS_CLIENT_EMAIL: str
    GS_CLIENT_ID: str
    GS_CLIENT: str
    GS_PRIVATE_KEY_ID: str
    GS_PRIVATE_KEY: str
    GS_PROJECT_ID: str
    GS_TOKEN_URI: str
    GS_TYPE: str
    JWT_EXPIRES_IN: int
    JWT_SECRET: str
    JWT_TEST_TOKEN: str


    def get_engine_uri(self, env: str = "test"):
        db_uri = ''

        if env == 'test':
            user = self.DATABASE_TEST_USER
            password = self.DATABASE_TEST_PASSWORD
            host = self.DATABASE_TEST_IP
            port = self.DATABASE_TEST_PORT
            name = self.DATABASE_TEST_NAME
        elif env == 'development':
            user = self.DATABASE_DEV_USER
            password = self.DATABASE_DEV_PASSWORD
            host = self.DATABASE_DEV_IP
            port = self.DATABASE_DEV_PORT
            name = self.DATABASE_DEV_NAME
        elif env == 'prod':
            user = self.DATABASE_PROD_USER
            password = self.DATABASE_PROD_PASSWORD
            host = self.DATABASE_PROD_IP
            port = self.DATABASE_PROD_PORT
            name = self.DATABASE_PROD_NAME

        db_uri = f'postgresql://{user}:{password}@{host}:{port}/{name}'
        return db_uri


class ConfigLoader:
    def __init__(self, config_file_path: typing.Optional[str]) -> None:
        self._config_file_path = config_file_path

    def _load_from_file(self) -> Config:
        assert self._config_file_path is not None
        with open(self._config_file_path, "rb") as file:
            data = tomllib.load(file)

        values = {}
        for field in dataclasses.fields(Config):
            try:
                if isinstance(field.type(),list):
                    values[field.name] = self.load_list(
                        data[field.name],
                        typing.get_args(field.type)[0])
                else :
                    values[field.name] = data[field.name]
            except KeyError:
                if field.default != dataclasses.MISSING:
                    values[field.name] = field.default
                else:
                    raise

        return Config(**values)

    def _load_from_env(self) -> Config:
        values = {}
        for field in dataclasses.fields(Config):
            try:
                if isinstance(field.type(),list):
                    values[field.name] = self.load_list(
                        environ[field.name.upper()],
                        typing.get_args(field.type)[0])
                else :
                    values[field.name] = environ[field.name.upper()]
            except KeyError:
                if field.default != dataclasses.MISSING:
                    values[field.name] = field.default
                else:
                    raise

        return Config(**values)

    def load_list(self, field: str, type: type = str) -> list:
        list_splited = field.split(",")
        result_list = []
        for element in list_splited:
            result_list.append(type(element.strip()))
        return result_list

    def load(self) -> Config:
        try:
            if self._config_file_path is not None:
                return self._load_from_file()
            return self._load_from_env()
        except KeyError as exc:
            raise ConfigEntryMissing(exc.args[0], self._config_file_path)

def get_config() -> Config:
    return ConfigLoader(environ.get("CONFIG_PATH", None)).load()

class ConfigLoaderError(Exception):
    pass


class ConfigEntryMissing(ConfigLoaderError):
    def __init__(self, entry: str, config_file_path: typing.Optional[str]) -> None:
        if config_file_path is not None:
            message = (
                f"Configuration entry '{entry}' is missing. "
                f"Please fill it in {config_file_path} configuration file "
                f"or through {entry.upper()} env var."
            )
        else:
            message = (
                f"Configuration entry '{entry}' is missing. "
                "Please fill it in configuration file and indicate "
                "configuration file path through CONFIG_PATH env var, "
                f"or fill this entry through {entry.upper()} env var."
            )
        super().__init__(message)
        self.entry = entry


