import yaml
import os


class ConfigReader:
    _config = None

    @classmethod
    def load_config(cls):
        if cls._config is None:
            project_root = os.path.dirname(os.path.dirname(__file__))

            config_path = os.path.join(
                project_root,
                "config",
                "config.yaml"
            )

            with open(config_path, "r") as file:
                cls._config = yaml.safe_load(file)

        return cls._config

    @classmethod
    def get(cls, section, key):
        config = cls.load_config()
        env = config["env"]
        return config[env][section][key]
