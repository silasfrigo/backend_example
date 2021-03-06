from pathlib import Path
from dynaconf import Dynaconf


PROJECT_DIR = Path(__file__).resolve().parent


settings = Dynaconf(
    envvar_prefix="PRESCRIPTIONS",
    environments=True,
    settings_files=[
        PROJECT_DIR / "settings.toml"
    ],
)
