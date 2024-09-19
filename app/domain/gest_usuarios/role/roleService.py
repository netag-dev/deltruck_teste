# roleService.py.py

from app.utils.singletonMeta import SingletonMeta

from .role import Role
from .roleRepository import RoleRepository


class RoleService(metaclass=SingletonMeta):
    def __init__(self):
        self.role_repository = RoleRepository()

    def get_all(self):
        return self.role_repository.find_all()

    def get_all_except_user_and_root(self):
        return self.role_repository.find_all_except_user_and_root()

    def get_by_name(self, name):
        return self.role_repository.find_by_name(name)
