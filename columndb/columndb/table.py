from .column import Column


class Table:
    def __init__(self, path='/tmp'):
        self.columnlist = {}
        # self.row_keys = set()
        self.path = path

    def put(self, col, key, value):
        if col not in self.columnlist:
            newcol = Column(col, self.path)
            self.columnlist[col] = newcol
        self.columnlist[col].add(key, value)
        
    def get(self, col, key):
        if col in self.columnlist:
            return self.columnlist[col].get(key)
        else:
            return None
