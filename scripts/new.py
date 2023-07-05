import os
dir = os.path.join(os.path.abspath(os.curdir),
                                  'data_temp')
print(dir)
print(os.listdir(dir))