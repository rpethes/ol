class UserData:
    def __init__(self):
        self._store = dict()
    
    def get(self, key):
        if (key in self._store.keys()):
            return self._store[key]
        return None
    
    def add(self, key, data):
        self._store[key] = data
        
    def hasKey(self, key):
        return( key in self._store )