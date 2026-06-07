import os
import sys

if __package__ is None and __name__ == "__main__":
    sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from Financeiro.config import DatabaseConfig
from Financeiro.database import Database
from Financeiro.controller.auth_controller import AuthController
from Financeiro.repository.user_repository import UserRepository
from Financeiro.view.login_view import LoginView


def main() -> None:
    config = DatabaseConfig()
    database = Database(config)
    repository = UserRepository(database)
    controller = AuthController(repository)
    view = LoginView(controller)
    view.run()


if __name__ == "__main__":
    main()
