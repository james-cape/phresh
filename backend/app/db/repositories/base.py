from databases import Database

class BaseRepository:
    '''
    Currently just a simple class to keep a reference to our db connection.
    '''
    def __init__(self, db: Database) -> None:
        self.db = db

