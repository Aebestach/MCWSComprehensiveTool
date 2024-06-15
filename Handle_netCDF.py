import numpy as np
import netCDF4 as nc
import tkinter as tk
from tkinter import filedialog


def handle_netCDF(file_path, selected_variables, adjust_longitude):
    root = tk.Tk()
    root.withdraw()

    save_path = filedialog.askdirectory()

    root.destroy()

    f = nc.Dataset(file_path)
    selected_variables = selected_variables.split(", ")
    for var in selected_variables:
        var_info = f.variables[var]
        var_data = f[var][:]
        var_data = np.array(var_data)
        if adjust_longitude:
            # Adjust the data from 0-360 longitude to -180 to 180 longitude
            mid_index = var_data.shape[3] // 2
            var_data = np.roll(var_data, shift=mid_index, axis=3)

        np.save(f"{save_path}/{var}.npy", var_data)
