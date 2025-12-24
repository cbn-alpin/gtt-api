import dataclasses
import tomllib
import typing
from os import environ


@dataclasses.dataclass
class Config:
    DATABASE_IP: str
    DATABASE_NAME: str
    DATABASE_PASSWORD: str
    DATABASE_PORT: str
    DATABASE_USER: str
    FLASK_APP: str
    FLASK_DEBUG: bool
    FLASK_ENV: str
    GS_AUTH_URI: str
    GS_CLIENT_ID: str
    GS_PRIVATE_KEY: str
    GS_TOKEN_URI: str
    JWT_EXPIRES_IN: int
    JWT_SECRET: str
    GEFIPROJ_URL: str
    GEFIPROJ_LOGIN: str
    GEFIPROJ_PASSWORD: str
    SQLALCHEMY_ENGINE_OPTIONS: dict = dataclasses.field(default_factory=lambda: {})
    SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
    JWT_BLACKLIST_ENABLED: bool = True
    JWT_BLACKLIST_TOKEN_CHECKS: list = dataclasses.field(default_factory=lambda: ["access"])

    def get_engine_uri(self):
        db_uri = ""

        user = self.DATABASE_USER
        password = self.DATABASE_PASSWORD
        host = self.DATABASE_IP
        port = self.DATABASE_PORT
        name = self.DATABASE_NAME

        db_uri = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"
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
            # Si le champ a une valeur par défaut, ne le chargez que s'il est présent.
            # Sinon, le champ est obligatoire.
            has_default = (
                field.default != dataclasses.MISSING
                or field.default_factory != dataclasses.MISSING
            )
            if field.name in data:
                if isinstance(field.type, type) and issubclass(field.type, list):
                    values[field.name] = self.load_list(data[field.name], typing.get_args(field.type)[0])
                else:
                    values[field.name] = data[field.name]
            elif not has_default:
                raise KeyError(field.name)

        return Config(**values)

    def _load_from_env(self) -> Config:
        values = {}
        for field in dataclasses.fields(Config):
            has_default = (
                field.default != dataclasses.MISSING
                or field.default_factory != dataclasses.MISSING
            )
            if field.name.upper() in environ:
                values[field.name] = environ[field.name.upper()]
            elif not has_default:
                raise KeyError(field.name)

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
    return ConfigLoader(environ.get("CONFIG_PATH", ".env")).load()


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
