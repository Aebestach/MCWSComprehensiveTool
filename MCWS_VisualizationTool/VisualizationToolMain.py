import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from plot_module import generate_and_save_plot
import json
import Generate_JSON
import os
import OutputLayers

data_type_mapping = {
    "Temperature": "ta",
    "Pressure": "hlpr",
    "Wind Speed": "ua",
    "Wind Speed(Direction)": "ua",
}


def UnlockControl(self):
    self.generate_button.config(state="disabled")
    self.galaxy_choice.config(state="normal")
    self.planet_choice.config(state="normal")
    self.bg_type_choice.config(state="normal")
    self.data_type_choice.config(state="normal")
    self.dim1_choice.config(state="normal")
    self.dim2_choice.config(state="normal")
    self.dpi_entry.config(state="normal")
    self.quality_choice.config(state="normal")


class MainApplication(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.title("MCWS Data Visualization Tool")
        self.geometry("680x720")

        for _ in range(1):
            tk.Label(self, text="").pack()

        frame = tk.Frame(self)
        frame.pack()
        title = tk.Label(frame, text="MCWS Data Visualization Tool", font=("Arial", 24))
        title.pack()

        for _ in range(1):
            tk.Label(self, text="").pack()

        # Galaxy and Planet selector
        galaxy_planet_frame = tk.Frame(self)
        galaxy_planet_frame.pack()
        tk.Label(galaxy_planet_frame, text="Select Galaxy:").pack(side="left")
        self.galaxy_choice = ttk.Combobox(galaxy_planet_frame, width=18)
        self.galaxy_choice.pack(side="left")
        self.galaxy_choice.bind("<<ComboboxSelected>>", self.update_planet_choice)

        tk.Label(galaxy_planet_frame, text="Select Planet:").pack(side="left")
        self.planet_choice = ttk.Combobox(galaxy_planet_frame, width=10)
        self.planet_choice.pack(side="right")
        self.planet_choice.bind("<<ComboboxSelected>>", self.update_type_choice)

        # Add multiple empty lines before the last two buttons
        for _ in range(2):
            tk.Label(self, text="").pack()

        # Background and Data type selector
        bg_data_type_frame = tk.Frame(self)
        bg_data_type_frame.pack()
        tk.Label(bg_data_type_frame, text="Background:").pack(side="left")
        self.bg_type_choice = ttk.Combobox(bg_data_type_frame, width=12)
        self.bg_type_choice.pack(side="left")

        tk.Label(bg_data_type_frame, text="Select Data:").pack(side="left")
        self.data_type_choice = ttk.Combobox(bg_data_type_frame, width=20)
        self.data_type_choice.pack(side="left")
        self.data_type_choice.bind("<<ComboboxSelected>>", self.update_Data_choice)

        arrow_numbers = ["Few", "Medium", "Intensive"]
        tk.Label(bg_data_type_frame, text="Number of Arrows:").pack(side="left")
        self.arrow_number_choice = ttk.Combobox(
            bg_data_type_frame, values=arrow_numbers, width=8, state="disabled"
        )
        self.arrow_number_choice.pack(side="left")

        # Add multiple empty lines before the last two buttons
        for _ in range(2):
            tk.Label(self, text="").pack()

        # Dimension selectors
        dimension_frame = tk.Frame(self)
        dimension_frame.pack()
        tk.Label(dimension_frame, text="Timestamp:").pack(side="left")
        self.dim1_choice = ttk.Combobox(dimension_frame, width=10)
        self.dim1_choice.pack(side="left")

        tk.Label(dimension_frame, text="Layer OR Altitude:").pack(side="left")
        self.layer_altitude_var = tk.StringVar()
        self.layer_altitude_choice = ttk.Combobox(
            dimension_frame,
            textvariable=self.layer_altitude_var,
            values=["Layers", "Altitude"],
            width=10,
        )
        self.layer_altitude_choice.pack(side="left")
        self.layer_altitude_choice.bind("<<ComboboxSelected>>", self.toggle_lock)

        for _ in range(1):
            tk.Label(self, text="").pack()

        Layer_Altitude_frame = tk.Frame(self)
        Layer_Altitude_frame.pack()
        tk.Label(Layer_Altitude_frame, text="Atmospheric Layers:").pack(side="left")
        self.dim2_choice = ttk.Combobox(
            Layer_Altitude_frame, width=10, state="disabled"
        )
        self.dim2_choice.pack(side="left")

        tk.Label(Layer_Altitude_frame, text="Sea-Level Altitude(m):").pack(side="left")
        self.altitude_entry = tk.Entry(Layer_Altitude_frame, width=8, state="disabled")
        self.altitude_entry.pack(side="left")

        # Add multiple empty lines before the last two buttons
        for _ in range(1):
            tk.Label(self, text="").pack()
        note3 = "Timestamp: Let's take Kerbin as an example,"
        note4 = "you can see 'timestepLength=2700' in MCWS_PlanetData/Binary/Stock/Kerbin/Kerbin.cfg data,"
        note5 = "which is in seconds (sec), so one timestamp would represent 2700 seconds (45 minutes), "
        note6 = "which means 24 timestamps is 3 days in Kerbin."
        note7 = "24×45÷[60 ×6(Kerbin hours)]=3"
        note8 = (
            "Atmospheric Layers: As the value increases, it gets closer to the surface."
        )
        note9 = "Sea-Level Altitude(m): Images can be drawn based on Altitude or Atmospheric Layers."
        note10 = "As you can see, only one of the two needs to be filled out."
        tk.Label(self, text=note3).pack()
        tk.Label(self, text=note4).pack()
        tk.Label(self, text=note5).pack()
        tk.Label(self, text=note6).pack()
        tk.Label(self, text=note7).pack()

        # Add multiple empty lines before the last two buttons
        for _ in range(1):
            tk.Label(self, text="").pack()

        tk.Label(self, text=note8).pack()
        tk.Label(self, text=note9).pack()
        tk.Label(self, text=note10, fg="red").pack()
        # Add multiple empty lines before the last two buttons
        for _ in range(1):
            tk.Label(self, text="").pack()
        # DPI and quality selectors
        dpi_quality_frame = tk.Frame(self)
        dpi_quality_frame.pack()
        tk.Label(dpi_quality_frame, text="DPI:").pack(side="left")
        self.dpi_entry = tk.Entry(dpi_quality_frame, width=8)
        self.dpi_entry.insert(0, "300")
        self.dpi_entry.pack(side="left")

        quality_levels = ["crude", "low", "intermediate", "high", "full"]
        tk.Label(dpi_quality_frame, text="SavedQuality:").pack(side="left")
        self.quality_choice = ttk.Combobox(
            dpi_quality_frame, values=quality_levels, width=13
        )
        self.quality_choice.set(quality_levels[0])
        self.quality_choice.pack(side="left")
        # Buttons
        # Add multiple empty lines before the last two buttons
        for _ in range(1):
            tk.Label(self, text="").pack()

        # Add a note about DPI and quality
        note1 = "Note: The higher the DPI and save quality, the slower the time to generate images. "
        note2 = (
            "It is recommended that the DPI default is 300 and the quality is crude."
        )

        tk.Label(self, text=note1).pack()
        tk.Label(self, text=note2, fg="red").pack()

        # Buttons
        # Add multiple empty lines before the last two buttons
        for _ in range(1):
            tk.Label(self, text="").pack()

        button_frame = tk.Frame(self)
        button_frame.pack()

        self.load_data_button = tk.Button(
            button_frame,
            text="Generate&Load Data",
            command=lambda: self.load_data(True),
        )
        self.load_data_button.pack(side="left", padx=10)

        # self.load_file_button = tk.Button(
        #     button_frame, text="Load Data", command=lambda: self.load_data(False)
        # )
        # self.load_file_button.pack(side="left", padx=10)

        self.check_button = tk.Button(
            button_frame, text="Check", command=self.check_data
        )
        self.check_button.pack(side="left", padx=5)

        self.generate_button = tk.Button(
            button_frame,
            text="Generate&Save Images",
            command=self.generate_image,
            state="disabled",
        )
        self.generate_button.pack(side="left", padx=10)

        self.clear_button = tk.Button(
            button_frame, text="Clear", command=self.clear_selections
        )
        self.clear_button.pack(side="left", padx=10)

    def update_planet_choice(self, event):
        # Clear selections
        self.planet_choice.set("")
        self.bg_type_choice.set("")
        self.data_type_choice.set("")
        self.dim1_choice.set("")
        self.dim2_choice.set("")
        self.arrow_number_choice.set("")
        self.layer_altitude_choice.set("")
        self.altitude_entry.delete(0, tk.END)
        self.dim2_choice["state"] = "disabled"
        self.altitude_entry["state"] = "disabled"
        galaxy = self.galaxy_choice.get()
        planets = self.galaxy_planet_data.get(galaxy, [])
        self.planet_choice.config(values=planets)

        self.planet_choice.bind("<<ComboboxSelected>>", self.update_type_choice)

    def update_type_choice(self, event):
        self.data_type_choice.set("")
        self.dim1_choice.set("")
        self.bg_type_choice.set("")
        planet = self.planet_choice.get()
        bg_types = self.bg_types.get(planet, [])
        self.bg_type_choice.config(values=bg_types)
        date_types = self.data_types.get(planet, [])
        self.data_type_choice.config(values=date_types)

    def update_Data_choice(self, event):
        planet = self.planet_choice.get()
        self.dim1_choice.set("")
        self.dim2_choice.set("")
        self.arrow_number_choice.set("")
        self.layer_altitude_choice.set("")
        self.altitude_entry.delete(0, tk.END)
        self.dim2_choice["state"] = "disabled"
        self.altitude_entry["state"] = "disabled"
        data_type = self.data_type_choice.get()
        if data_type:
            dim1_values = self.dim1_data[planet].get(data_type_mapping[data_type], [])
            dim1_values = (
                [str(i) for i in range(1, dim1_values + 1)] if dim1_values else []
            )
            self.dim1_choice.config(values=dim1_values)

            # Set the default values to the first and last numbers of the array
            if dim1_values:
                self.dim1_choice.set(dim1_values[0])

            # Unlock the arrow_number_choice widget if data_type is 'Wind Speed(Direction)'
            if data_type == "Wind Speed(Direction)":
                self.arrow_number_choice.config(state="normal")
                self.arrow_number_choice.set("Medium")
            else:
                self.arrow_number_choice.config(state="disabled")

    def toggle_lock(self, event):
        if self.layer_altitude_var.get() == "Layers":
            self.dim2_choice.set("")

            planet = self.planet_choice.get()
            bg_types = self.bg_types.get(planet, [])
            self.bg_type_choice.config(values=bg_types)

            data_type = self.data_type_choice.get()
            if data_type:
                dim2_values = self.dim2_data[planet].get(
                    data_type_mapping[data_type], []
                )
                dim2_values = (
                    [str(i) for i in range(1, dim2_values + 1)] if dim2_values else []
                )
                self.dim2_choice.config(values=dim2_values)

                # Set the default values to the first and last numbers of the array
                if self.dim1_choice.get():
                    self.dim2_choice.set(dim2_values[-1])
            self.altitude_entry.delete(0, tk.END)
            self.dim2_choice["state"] = "normal"
            self.altitude_entry["state"] = "disabled"
        else:
            self.dim2_choice["state"] = "disabled"
            self.altitude_entry["state"] = "normal"
            self.dim2_choice.set("")

    def clear_selections(self):
        self.galaxy_choice.set("")
        self.planet_choice.set("")
        self.bg_type_choice.set("")
        self.data_type_choice.set("")
        self.dim1_choice.set("")
        self.dim2_choice.set("")
        self.arrow_number_choice.set("")
        self.layer_altitude_choice.set("")
        self.altitude_entry.config(state="normal")
        self.altitude_entry.delete(0, tk.END)

        UnlockControl(self)

        self.generate_button.config(state="disabled")
        self.arrow_number_choice.config(state="disabled")
        self.dim2_choice.config(state="disabled")
        self.altitude_entry.config(state="disabled")
        self.layer_altitude_choice.config(state="normal")

    def load_data_from_json(self, file_path):
        with open(file_path, "r") as f:
            data = json.load(f)
        return data

    def load_data(self, generate_json_file=True):
        Generate_JSON.generate_json()

        # Read all .json files from the Data/Saved_json folder
        folder_path = "Data/Saved_json"
        json_files = [f for f in os.listdir(folder_path) if f.endswith(".json")]

        # Fill in the name of the JSON file in the drop-down box of galaxy_choice
        galaxy_names = [os.path.splitext(f)[0] for f in json_files]
        self.galaxy_choice.config(values=galaxy_names)

        self.galaxy_planet_data = {}
        self.bg_types = {}
        self.dim1_data = {}
        self.dim2_data = {}
        self.longitudeOffset = {}
        self.scaleFactor = {}
        self.modelTop = {}
        self.data_types = {}

        for json_file in json_files:
            file_path = os.path.join(folder_path, json_file)
            data = self.load_data_from_json(file_path)

            galaxy = os.path.splitext(json_file)[
                0
            ]  # Get the galaxy name from the file name
            for planet, details in data[
                galaxy
            ].items():  # Use the galaxy name to access the data
                self.galaxy_planet_data.setdefault(galaxy, []).append(planet)
                if galaxy == "TidallyLockedKerbin":
                    planet = "TLKerbin"
                self.bg_types[planet] = details["Background"]
                self.dim1_data[planet] = details["FirstDimension"]
                self.dim2_data[planet] = details["SecondDimension"]
                self.longitudeOffset[planet] = details["longitudeOffset"]
                self.scaleFactor[planet] = details["scaleFactor"]
                self.modelTop[planet] = details["modelTop"]
                self.data_types[planet] = details["data_types"]

    def check_data(self):
        if self.layer_altitude_choice.get() == "Layers":
            choices = [
                self.galaxy_choice,
                self.planet_choice,
                self.bg_type_choice,
                self.data_type_choice,
                self.dim1_choice,
                self.dim2_choice,
                self.dpi_entry,
                self.quality_choice,
            ]
        elif self.layer_altitude_choice.get() == "Altitude":
            choices = [
                self.galaxy_choice,
                self.planet_choice,
                self.bg_type_choice,
                self.data_type_choice,
                self.dim1_choice,
                self.altitude_entry,
                self.dpi_entry,
                self.quality_choice,
            ]
            if int(self.altitude_entry.get()) < 0:
                messagebox.showinfo("Attention", "Abnormal height values!")
                return
        elif self.layer_altitude_choice.get() == "":
            messagebox.showinfo("Attention", "Please select layer or altitude")
            return

        for choice in choices:
            if isinstance(choice, ttk.Combobox):
                if not choice.get():  # If Combobox is empty
                    messagebox.showinfo(
                        "Attention", "Please continue to fill in the information."
                    )
                    return
            elif isinstance(choice, tk.Entry):
                if not choice.get():  # If Entry is empty
                    messagebox.showinfo(
                        "Attention", "Please continue to fill in the information."
                    )
                    return

        self.generate_button.config(state="normal")
        self.galaxy_choice.config(state="disabled")
        self.planet_choice.config(state="disabled")
        self.bg_type_choice.config(state="disabled")
        self.data_type_choice.config(state="disabled")
        self.dim1_choice.config(state="disabled")
        self.dim2_choice.config(state="disabled")
        self.dpi_entry.config(state="disabled")
        self.quality_choice.config(state="disabled")
        self.arrow_number_choice.config(state="disabled")
        self.altitude_entry.config(state="disabled")
        self.layer_altitude_choice.config(state="disabled")
        return True

    def generate_image(self):
        galaxy = self.galaxy_choice.get()
        planet = self.planet_choice.get()
        bg_type = self.bg_type_choice.get()
        data_type = self.data_type_choice.get()
        dim1 = int(self.dim1_choice.get())

        model_top = self.modelTop[planet].get(data_type_mapping[data_type], {})
        scale_factor = self.scaleFactor[planet].get(data_type_mapping[data_type], {})
        dim2 = self.dim2_data[planet].get(data_type_mapping[data_type], {})
        if self.layer_altitude_choice.get() == "Layers":
            dim2 = int(self.dim2_choice.get())
        else:
            dim3=dim2
            dim2 = OutputLayers.output_layers(
                float(self.altitude_entry.get()),
                float(model_top),
                float(scale_factor),
                int(dim2),
            )
            dim2=dim3-dim2
        dpi = self.dpi_entry.get()
        quality = self.quality_choice.get()
        arrow_number = self.arrow_number_choice.get()

        try:
            # A Save File dialog box pops up, allowing the user to select a save location
            directory = filedialog.askdirectory()
            if not directory:
                return  # The user canceled the save

            longitudeOffset = self.longitudeOffset[planet].get(
                data_type_mapping[data_type], []
            )
            generate_and_save_plot(
                galaxy,
                planet,
                bg_type,
                data_type,
                dim1 - 1,
                dim2 - 1,
                int(dpi),
                quality,
                directory,
                arrow_number,
                longitudeOffset,
            )
            messagebox.showinfo(
                "Success", "The image was generated and saved successfully!"
            )
        except Exception as e:
            messagebox.showerror("Wrong", f"Failed to generate image: {e}")

        UnlockControl(self)
        self.layer_altitude_choice.config(state="normal")
        self.layer_altitude_choice.set("")
        self.dim2_choice.set("")
        self.altitude_entry.config(state="normal")
        self.altitude_entry.delete(0, tk.END)
        self.dim2_choice.config(state="disabled")
        self.altitude_entry.config(state="disabled")
        if data_type == "Wind Speed(Direction)":
            self.arrow_number_choice.config(state="normal")
        else:
            self.arrow_number_choice.config(state="disabled")


if __name__ == "__main__":
    app = MainApplication()
    app.mainloop()
