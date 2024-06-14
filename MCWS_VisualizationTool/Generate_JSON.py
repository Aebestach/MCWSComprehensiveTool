import os
import json
import numpy as np
import re


def get_subdirectories(directory):
    return {
        name: {
            "Background": ["Topography", "Visual", "Mapless"],
            "FirstDimension": {"hlpr": [], "ta": [], "ua": []},
            "SecondDimension": {"hlpr": [], "ta": [], "ua": []},
            "longitudeOffset": {"hlpr": None, "ta": None, "ua": None},
            "scaleFactor": {"hlpr": None, "ta": None, "ua": None},
            "modelTop": {"hlpr": None, "ta": None, "ua": None},
            "sizeAlt": {"hlpr": None, "ta": None, "ua": None},
            "data_types": [
                "Temperature",
                "Pressure",
                "Wind Speed",
                "Wind Speed(Direction)",
            ],
        }
        for name in os.listdir(directory)
        if os.path.isdir(os.path.join(directory, name)) and name != "Patches"
    }


def load_data(directory, data, background_directory):
    for subdir, content in data.items():
        for dimension in ["FirstDimension", "SecondDimension"]:
            for key in content[dimension]:
                file_path = os.path.join(directory, subdir, f"{key}.npy")
                if os.path.isfile(file_path):
                    data_array = np.load(file_path)
                    if dimension == "FirstDimension":
                        content[dimension][key] = data_array.shape[0]
                    elif dimension == "SecondDimension":
                        content[dimension][key] = data_array.shape[1]
                else:
                    content[dimension][key] = None
        for bg_dir in os.listdir(background_directory):
            for key in ["Topography", "Visual", "Mapless", "Coastline"]:
                file_path = os.path.join(background_directory, bg_dir, subdir, key)
                if os.path.isfile(file_path + ".png"):
                    if key == "Coastline" and key not in content["Background"]:
                        content["Background"].insert(
                            content["Background"].index("Mapless"), key
                        )
    return data


def load_cfg(directory, data):
    cfg_map = {"Wind_Data": "ua", "Temperature_Data": "ta", "Pressure_Data": "hlpr"}
    data_type_map = {
        "Wind_Data": ["Wind Speed", "Wind Speed(Direction)"],
        "Temperature_Data": ["Temperature"],
        "Pressure_Data": ["Pressure"],
    }

    for subdir, content in data.items():
        subdir_path = os.path.join(directory, subdir)
        for root, _, files in os.walk(subdir_path):
            for file in files:
                if file.endswith(".cfg"):
                    cfg_path = os.path.join(root, file)
                    with open(cfg_path, "r") as f:
                        cfg_content = f.read()

                    # 移除注释行
                    cfg_content = re.sub(r"//.*", "", cfg_content)
                    cfg_content = re.sub(
                        r"@\w+:\w+\[.*?\]:\w+\[.*?\]\s*{", "", cfg_content
                    )

                    for cfg_name, key in cfg_map.items():
                        if cfg_name in cfg_content:
                            match = re.search(
                                rf"{cfg_name}.*?longitudeOffset\s*=\s*(\d+(\.\d+)?)",
                                cfg_content,
                                re.DOTALL,
                            )
                            if match:
                                content["longitudeOffset"][key] = float(match.group(1))
                            match = re.search(
                                rf"{cfg_name}.*?scaleFactor\s*=\s*(\d+(\.\d+)?)",
                                cfg_content,
                                re.DOTALL,
                            )
                            if match:
                                content["scaleFactor"][key] = float(match.group(1))
                            match = re.search(
                                rf"{cfg_name}.*?modelTop\s*=\s*(\d+(\.\d+)?)",
                                cfg_content,
                                re.DOTALL,
                            )
                            if match:
                                content["modelTop"][key] = float(match.group(1))
                            match = re.search(
                                rf"{cfg_name}.*?sizeAlt\s*=\s*(\d+(\.\d+)?)",
                                cfg_content,
                                re.DOTALL,
                            )
                            if match:
                                content["sizeAlt"][key] = float(match.group(1))
                        else:
                            for data_type in data_type_map[cfg_name]:
                                if data_type in content["data_types"]:
                                    content["data_types"].remove(data_type)
    return data


def create_json(directory, output_directory, background_directory):
    for subdir in os.listdir(directory):
        if os.path.isdir(os.path.join(directory, subdir)) and subdir != "Patches":
            subdir_data = get_subdirectories(os.path.join(directory, subdir))
            subdir_data = load_data(
                os.path.join(directory, subdir), subdir_data, background_directory
            )
            subdir_data = load_cfg(os.path.join(directory, subdir), subdir_data)
            clean_data_types(subdir_data)
            data = {subdir: subdir_data}
            with open(
                os.path.join(output_directory, f"{subdir}.json"), "w", encoding="utf-8"
            ) as f:
                json.dump(data, f, ensure_ascii=False, indent=4)


def clean_data_types(data):
    for subdir, content in data.items():
        if "Temperature" not in content["data_types"]:
            del content["FirstDimension"]["ta"]
            del content["SecondDimension"]["ta"]
            del content["longitudeOffset"]["ta"]
            del content["scaleFactor"]["ta"]
            del content["modelTop"]["ta"]
            del content["sizeAlt"]["ta"]

        if "Pressure" not in content["data_types"]:
            del content["FirstDimension"]["hlpr"]
            del content["SecondDimension"]["hlpr"]
            del content["longitudeOffset"]["hlpr"]
            del content["scaleFactor"]["hlpr"]
            del content["modelTop"]["hlpr"]
            del content["sizeAlt"]["hlpr"]

        if not any(
            wind in content["data_types"]
            for wind in ["Wind Speed", "Wind Speed(Direction)"]
        ):
            del content["FirstDimension"]["ua"]
            del content["SecondDimension"]["ua"]
            del content["longitudeOffset"]["ua"]
            del content["scaleFactor"]["ua"]
            del content["modelTop"]["ua"]
            del content["sizeAlt"]["ua"]


def generate_json():
    create_json(
        "Data/MCWS_PlanetData/Binary", "Data/Saved_json", "Data/PlanetBackground"
    )
