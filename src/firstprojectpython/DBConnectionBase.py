from typing import Protocol

class DBConnectionBase(Protocol):
    def retrieve_cities(self):
        pass