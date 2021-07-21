from flask import session, request

from Util.subpages import SignIn


class User(SignIn):

    def __init__(self):
        super().__init__()
        self._usr = request.form.get("usr")
        self._pwd = request.form.get("pwd")

    def get_usr(self):
        return self._usr

    def get_pwd(self):
        return self._pwd

    def correct_identity(self):
        if self._if_in_db_where(self.get_pwd(),
                                self.table,
                                "Passwd",
                                pair=["Username", self.get_usr()]):
            return True
        else:
            return False

    def create_session(self):
        session['usr_info'] = self.get_usr()

    def has_duplicate(self):
        if self._if_in_db(self.get_usr(), self.table, "Username"):
            return True
        else:
            return False

    def create_usr(self):
        self._ins(self.table,
                  {"field": "Username", "value": self.get_usr()},
                  {"field": "Passwd", "value": self.get_pwd()})
        self._commit()





