# utils/singletonMeta.py

class SingletonMeta(type):
    """Metaclasse para implementar o padrão Singleton."""
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super().__call__(*args, **kwargs)
        return cls._instances[cls]
