import os


POSTFIX_DATA = '.data'
POSTFIX_INDX = '.idx'

class SSTable:
    """
    the set of SSTable
    """
    def __init__(self, mem_dict, file_name):
        self.file_name = file_name
        mem_list = []
        if isinstance(mem_dict, dict):
            for key in mem_dict:
                mem_list.append((key, mem_dict[key]))
        else:
            mem_list = mem_dict

        mem_list.sort()
        with open(self.file_name + POSTFIX_DATA, 'w') as fp_data:
            with open(self.file_name + POSTFIX_INDX, 'w') as fp_index:
                next_offset = 0
                for key,value in mem_list:
                    current_item = f"{key}\t{value}\n"

                    fp_data.write(current_item)
                    fp_index.write(f"{key}\t{next_offset}\n")
                    next_offset += len(current_item)

    # def check(self, key):
    #     with open(self.file_name + POSTFIX_DATA, 'r') as fp_index:
    #         index = [line.split("\t") for line in fp_index.readlines()]
    #         for k,v in index:
    #             if k == key:
    #                 return (key, int(v.rstrip()))

    #     return (key, -1)

    def get(self, key):
        # offset = self.check(key)[1]
        # if offset > -1:
        #     with open(self.file_name + "_data.dat", 'r') as fp_data:
        #         fp_data.seek(offset, 0)
        #         data = fp_data.readline().split('\t')[1].rstrip()
        #         return data
        # return None
        with open(self.file_name + POSTFIX_INDX, 'r') as fp_index:
            index = [line.split("\t") for line in fp_index.readlines()]
            for k,v in index:
                if k == key:
                    offset = int(v.rstrip())
                    with open(self.file_name + POSTFIX_DATA, 'r') as fp_data:
                        fp_data.seek(offset, 0)
                        data = fp_data.readline().split('\t')[1].rstrip()
                        return data

        return None

    def to_list(self):
        result = []
        with open(self.file_name + POSTFIX_DATA, 'r') as fp_data:
            index = [line.split('\t') for line in fp_data.readlines()]
            for k,v in index:
                result.append((k, v.rstrip()))
        
        return result

    def remove(self):
        os.remove(self.file_name + POSTFIX_DATA)
        os.remove(self.file_name + POSTFIX_INDX)
