from mysql.connector.errors import Error as MySQLError


class InsertOwnerError(Exception):
    sql_error: MySQLError
    msg: str

    def __init__(self, sql_error: MySQLError):
        self.sql_error = sql_error
        if sql_error.errno == 1048:
            self.msg = 'Użytkownik musi mieć poprawny numer telefonu'
        elif sql_error.errno == 1062:
            self.msg = 'Użytkownik z takim numerem już istnieje'
        elif sql_error.errno == 1406:
            self.msg = 'Jedno z pól ma za dużo znaków'
        else:
            self.msg = 'Błąd: ' + sql_error.msg


class InsertDogError(Exception):
    sql_error: MySQLError
    msg: str

    def __init__(self, sql_error: MySQLError):
        self.sql_error = sql_error
        if sql_error.errno == 1048:
            self.msg = 'Pies musi mieć podaną rasę i wielkość'
        elif sql_error.errno == 1406:
            self.msg = 'Jedno z pól ma za dużo znaków'
        else:
            self.msg = 'Błąd: ' + sql_error.msg


class EditDogError(Exception):
    sql_error: MySQLError
    msg: str

    def __init__(self, sql_error: MySQLError):
        self.sql_error = sql_error
        if sql_error.errno == 1406:
            self.msg = 'Jedno z pól ma za dużo znaków'
        else:
            self.msg = 'Błąd: ' + sql_error.msg


class EditOwnerError(Exception):
    sql_error: MySQLError
    msg: str

    def __init__(self, sql_error: MySQLError):
        self.sql_error = sql_error
        if sql_error.errno == 1048:
            self.msg = 'Użytkownik musi mieć poprawny numer telefonu'
        elif sql_error.errno == 1062:
            self.msg = 'Użytkownik z takim numerem już istnieje'
        elif sql_error.errno == 1406:
            self.msg = 'Jedno z pól ma za dużo znaków'
        else:
            self.msg = 'Błąd: ' + sql_error.msg


class InsertAppointmentError(Exception):
    sql_error: MySQLError
    msg: str

    def __init__(self, sql_error: MySQLError):
        self.sql_error = sql_error
        if sql_error.errno == 1048:
            self.msg = 'Wizyta musi mieć wybraną usługę'
        else:
            self.msg = 'Błąd: ' + sql_error.msg
