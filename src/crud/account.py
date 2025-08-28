from crud.base import CRUDBase
from models import Account


class CRUDAccount(CRUDBase):
    pass


account_crud = CRUDAccount(Account)
