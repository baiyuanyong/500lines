from .memtable import MEMTable
from .sstable import SSTable
import os


MERGE_THRESHOLD = 10

class Column:
    def __init__(self, col_name, path):
        self.col_name = col_name
        self.small_index = 0
        self.bigFile = []
        self.smallFile = []
        self.mt = MEMTable()
        # self.path = f"/tmp/{self.col_name}"
        self.path = path + '/' + col_name
        if not os.path.isdir(self.path):
            os.mkdir(self.path)

    def add(self, key, value):
        flush = self.mt.add(key, value)
        if flush:
            self.persist()

    def get(self, key):
        result = self.mt.get(key)
        if result is not None:
            return result

        for sstable in reversed(self.smallFile):
            result = sstable.get(key)
            if result is not None:
                return result


        for sstable in reversed(self.bigFile):
            result = sstable.get(key)
            if result is not None:
                return result

        return None

    def persist(self):
        # sst = SSTable(self.mt.table, f"{self.path}/small_{len(self.smallFile)}") 
        sst = SSTable(self.mt.table, f"{self.path}/small_{self.small_index}")
        self.small_index += 1
        self.smallFile.append(sst)
        self.mt.clear()
        if len(self.smallFile)>=MERGE_THRESHOLD:
            self.compact()

    def compact(self):
        sstable_list = []
        for sstable in self.smallFile:
            sstable_list.extend(sstable.to_list())
        sst = SSTable(sstable_list, f"{self.path}/big_{len(self.bigFile)}")
        self.bigFile.append(sst)

        for sstable in self.smallFile:
            sstable.remove()
        self.smallFile = []
