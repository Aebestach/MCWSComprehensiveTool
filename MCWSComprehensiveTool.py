import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import Handle_netCDF
import HandleData
import HandleImage
import math

def handle_netcdf_to_npz():
    file_path = filedialog.askopenfilename(filetypes=[("NetCDF Files", "*.nc")])
    if file_path:
        selected_variables = ", ".join(
            [var.get() for var in variable_vars if var.get()]
        )
        adjust_longitude = adjust_longitude_var.get()
        try:
            Handle_netCDF.handle_netCDF(file_path, selected_variables, adjust_longitude)
            messagebox.showinfo("Success", "The '.npy' file generation complete!")
        except Exception as e:
            messagebox.showerror("Wrong", f"Failed to generate: {e}")


def handle_kspmap():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.dds")])
    if file_path:
        try:
            HandleImage.handle_KSP(file_path)
            messagebox.showinfo("Success", "Modified successfully!")
        except Exception as e:
            messagebox.showerror("Wrong", f"Modification Failure: {e}")


def handle_exoplasimmap():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png;*.dds")])
    if file_path:
        try:
            HandleImage.handle_ExoPlaSim(file_path)
            messagebox.showinfo("Success", "Modified successfully!")
        except Exception as e:
            messagebox.showerror("Wrong", f"Modification Failure: {e}")


def handle_coastline():
    file_path = filedialog.askopenfilename(filetypes=[("Image Files", "*.png")])
    if file_path:
        try:
            HandleImage.handle_coatline(file_path)
            messagebox.showinfo("Success", "Modified successfully!")
        except Exception as e:
            messagebox.showerror("Wrong", f"Modification Failure: {e}")


def handle_unlocked_button():
    # Check if any variable is selected
    any_selected = any(var.get() for var in variable_vars)
    if any_selected:
        netcdf_to_npz_button.config(state="normal")
    else:
        netcdf_to_npz_button.config(state="disabled")


def handle_npy_files():
    file_paths = filedialog.askopenfilenames(filetypes=[("Numpy Files", "*.npy")])
    if file_paths:
        try:
            HandleData.HandleData(file_paths)
            messagebox.showinfo("Success", "Processing completed!")
        except Exception as e:
            messagebox.showerror("Wrong", f"Processing failure: {e}")


def Calculate():
    lon_asc_node = longitudeOfAscendingNode.get()
    arg_periapsis = argumentOfPeriapsis.get()
    mean_anomaly = meanAnomalyAtEpochD.get()
    init_rotation = initialRotation.get()
    mean_anomaly= float(mean_anomaly) *180 / math.pi
    result=float(lon_asc_node)+ float(arg_periapsis)+ mean_anomaly- float(init_rotation)-180
    result_label.insert(0,str(result))


# List of variables for check buttons
variables = ["ta", "ua", "va", "wa", "hlpr"]

# Initialize the main window
root = tk.Tk()
root.title("MCWS Comprehensive Tool")

# Frame for the first button and its controls
frame1 = ttk.Frame(root)
frame1.pack(padx=10, pady=10, fill="x")

# Check buttons for Variables
variable_vars = []
for var in variables:
    var_check = tk.StringVar()
    check_button = ttk.Checkbutton(
        frame1,
        text=var,
        variable=var_check,
        onvalue=var,
        offvalue="",
        command=handle_unlocked_button,
    )
    check_button.pack(side="left", padx=5)
    variable_vars.append(var_check)

# Radio button for Adjust Longitude
adjust_longitude_var = tk.BooleanVar(value=False)
adjust_longitude_radio = ttk.Checkbutton(
    frame1, text="Adjust Longitude", variable=adjust_longitude_var
)
adjust_longitude_radio.pack(side="left", padx=5)

# Button for netCDF -> npz
netcdf_to_npz_button = ttk.Button(
    frame1, text="netCDF->npy", command=handle_netcdf_to_npz
)
netcdf_to_npz_button.pack(side="left", padx=10)
netcdf_to_npz_button.config(state="disabled")


# Frame for the second and third buttons
frame2 = ttk.Frame(root)
frame2.pack(padx=10, pady=10, fill="x")

# Configure grid layout for frame2
frame2.columnconfigure(0, weight=1)
frame2.columnconfigure(1, weight=1)
frame2.columnconfigure(2, weight=1)
# Button for KSPMap
kspmap_button = ttk.Button(frame2, text="Pic->KSPMap", command=handle_kspmap)
kspmap_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew")

# Button for ExoPlaSimMap
exoplasimmap_button = ttk.Button(
    frame2, text="Pic->ExoPlaSimMap", command=handle_exoplasimmap, state="disabled"
)
exoplasimmap_button.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

# Button for ExoPlaSimMap
draw_coastline = ttk.Button(frame2, text="DrawCoastline", command=handle_coastline)
draw_coastline.grid(row=0, column=2, padx=5, pady=5, sticky="ew")

note1 = "Pic should be png or dds from Kittopia or planet packs"
note2 = "Please pass a PNG with black land and transparent ocean for coastline drawing"
note3 = "DrawCoastline will automatically convert to the correct KSP need Map"
label = tk.Label(frame2, text=note1)
label.grid(row=1, column=0, padx=5, pady=5, sticky="ew", columnspan=3)
label = tk.Label(frame2, text=note2, fg="red")
label.grid(row=2, column=0, padx=5, pady=5, sticky="ew", columnspan=3)
label = tk.Label(frame2, text=note3)
label.grid(row=3, column=0, padx=5, pady=5, sticky="ew", columnspan=3)

# Frame for the third set of controls
frame3 = ttk.Frame(root)
frame3.pack(padx=10, pady=10, fill="x")

# Configure grid layout for frame3
frame3.columnconfigure(0, weight=1)
frame3.columnconfigure(1, weight=1)
# New button for handling .npy files
handle_npy_button = ttk.Button(
    frame3, text="Handle .npy Files", command=handle_npy_files
)
handle_npy_button.grid(row=0, column=0, padx=5, pady=5, sticky="ew", columnspan=2)
handle_npy_button.config(state="disabled")


# Frame for the third set of controls
frame4 = ttk.Frame(root)
frame4.pack(padx=10, pady=10, fill="x")
frame4.columnconfigure(0, weight=1)
frame4.columnconfigure(1, weight=1)
frame4.columnconfigure(2, weight=1)
frame4.columnconfigure(3, weight=1)

note5 = "Directly fill in the orbital roots from the planet configuration or"
note6 = "the data displayed by HyperEdit in the input box below."
label = tk.Label(frame4, text=note5)
label.grid(row=0, column=0, padx=5, pady=5, sticky="ew", columnspan=4)
label = tk.Label(frame4, text=note6)
label.grid(row=1, column=0, padx=5, pady=5, sticky="ew", columnspan=4)

ttk.Label(frame4, text="longitudeOfAscendingNode:").grid(row=3, column=0, sticky="e")
longitudeOfAscendingNode = ttk.Entry(frame4, width=5)
longitudeOfAscendingNode.grid(row=3, column=1, padx=5, pady=5, sticky="ew")

ttk.Label(frame4, text="argumentOfPeriapsis:").grid(row=3, column=2, sticky="e")
argumentOfPeriapsis = ttk.Entry(frame4, width=5)
argumentOfPeriapsis.grid(row=3, column=3, padx=5, pady=5, sticky="ew")

ttk.Label(frame4, text="meanAnomalyAtEpochD (radian):").grid(
    row=4, column=0, sticky="e"
)
meanAnomalyAtEpochD = ttk.Entry(frame4, width=5)
meanAnomalyAtEpochD.grid(row=4, column=1, padx=5, pady=5, sticky="ew")

ttk.Label(frame4, text="initialRotation:").grid(row=4, column=2, sticky="e")
initialRotation = ttk.Entry(frame4, width=5)
initialRotation.grid(row=4, column=3, padx=5, pady=5, sticky="ew")

visualization_tool_button = ttk.Button(
    frame4, text="Calculate Substellar Point", command=Calculate
)
visualization_tool_button.grid(
    row=5, column=0, padx=5, pady=5, sticky="ew", columnspan=4
)

ttk.Label(frame4, text="Substellar Point:").grid(row=6, column=0, sticky="e", columnspan=1)
result_label = ttk.Entry(frame4, width=20)
result_label.grid(row=6, column=1, padx=5, pady=5, sticky="ew", columnspan=2)
ttk.Label(frame4, text="°").grid(row=6, column=3, sticky="w", columnspan=1)

# Start the main event loop
root.mainloop()
