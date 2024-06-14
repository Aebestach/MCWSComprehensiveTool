import numpy as np

def HandleData(file_paths):
    for file_path in file_paths:
        data = np.load(file_path)
        mid_index = data.shape[3] // 2
        data = np.roll(data, shift=mid_index, axis=3)
        np.save(file_path, data)
