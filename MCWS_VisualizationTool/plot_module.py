import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import inflect

p = inflect.engine()

PlongitudeOffset = 0


def generate_and_save_plot(
    galaxy,
    planet,
    bg_type,
    data_type,
    dim1,
    dim2,
    dpi,
    quality,
    directory,
    arrow_number,
    longitudeOffset,
):
    global PlongitudeOffset
    PlongitudeOffset = longitudeOffset+180

    quality = quality_switch(quality)
    file_name = f"Data/MCWS_PlanetData/Binary/{galaxy}/{planet}"
    background_name = get_background_name(galaxy, planet, bg_type)

    if data_type in ["Wind Speed", "Wind Speed(Direction)"]:
        draw_wind_speed(
            planet,
            bg_type,
            data_type,
            dim1,
            dim2,
            dpi,
            quality,
            directory,
            file_name,
            background_name,
            arrow_number,
        )
    else:
        draw_temperature_and_pressure(
            planet,
            bg_type,
            data_type,
            dim1,
            dim2,
            dpi,
            quality,
            directory,
            file_name,
            background_name,
        )


def draw_temperature_and_pressure(
    planet,
    bg_type,
    data_type,
    dim1,
    dim2,
    dpi,
    quality,
    file_path,
    file_name,
    background_name,
):
    data_file_name = (
        f"{file_name}/ta.npy" if data_type == "Temperature" else f"{file_name}/hlpr.npy"
    )
    data = np.load(data_file_name)
    ordinal_layer = p.ordinal(data.shape[1] - dim2)
    pic_name = f"{planet} Timestamp-{dim1+1} {ordinal_layer}-Layer {data_type}"
    valid_data = prepare_data(data, dim1, dim2)
    draw_map(
        bg_type,
        data_type,
        valid_data,
        quality,
        background_name,
        pic_name,
        file_path,
        dpi,
    )


def draw_wind_speed(
    planet,
    bg_type,
    data_type,
    dim1,
    dim2,
    dpi,
    quality,
    file_path,
    file_name,
    background_name,
    arrow_number,
):
    data_ua = np.load(f"{file_name}/ua.npy")
    data_va = np.load(f"{file_name}/va.npy")
    data_wa = np.load(f"{file_name}/wa.npy")
    ordinal_layer = p.ordinal(data_ua.shape[1] - dim2)
    if data_type == "Wind Speed(Direction)":
        pic_name = f"{planet} Timestamp-{dim1+1} {ordinal_layer}-Layer {data_type}-{arrow_number}"
    else:
        pic_name = f"{planet} Timestamp-{dim1+1} {ordinal_layer}-Layer {data_type}"

    wind_data_ua, wind_data_va, wind_data_wa = prepare_wind_data(
        data_ua, data_va, data_wa, dim1, dim2
    )
    total_wind_speed = calculate_total_wind_speed(
        data_type, wind_data_ua, wind_data_va, wind_data_wa
    )
    draw_map(
        bg_type,
        data_type,
        total_wind_speed,
        quality,
        background_name,
        pic_name,
        file_path,
        dpi,
        wind_data_ua,
        wind_data_va,
        arrow_number,
    )


def get_background_name(galaxy, planet, bg_type):
    bg_name = f"Data/PlanetBackground/{galaxy}/{planet}"
    return {
        "Topography": f"{bg_name}/Topography.png",
        "Visual": f"{bg_name}/Visual.png",
        "Coastline": f"{bg_name}/Coastline.png",
        "Mapless": None,
    }.get(bg_type)


def quality_switch(quality):
    return {
        "crude": "c",
        "low": "l",
        "intermediate": "i",
        "high": "h",
        "full": "f",
    }.get(quality)


def prepare_data(data, dim1, dim2):
    valid_data = data[dim1, dim2, :, :]
    indexOffset = int(PlongitudeOffset / (360 / valid_data.shape[1]))
    return np.roll(valid_data, shift=indexOffset, axis=1)


def prepare_wind_data(data_ua, data_va, data_wa, dim1, dim2):
    wind_data_ua = prepare_data(data_ua, dim1, dim2)
    wind_data_va = prepare_data(data_va, dim1, dim2)
    wind_data_wa = prepare_data(data_wa, dim1, dim2)
    return wind_data_ua, wind_data_va, wind_data_wa


def calculate_total_wind_speed(data_type, wind_data_ua, wind_data_va, wind_data_wa):
    if data_type == "Wind Speed":
        return np.sqrt(wind_data_ua**2 + wind_data_va**2 + wind_data_wa**2)
    else:
        return np.sqrt(wind_data_ua**2 + wind_data_va**2)


def draw_map(
    bg_type,
    data_type,
    valid_data,
    quality,
    background_name,
    pic_name,
    file_path,
    dpi,
    wind_data_ua=None,
    wind_data_va=None,
    arrow_number=None,
):
    lon, lat = np.meshgrid(
        np.linspace(-180, 180, valid_data.shape[1]),
        np.linspace(90, -90, valid_data.shape[0]),
    )
    fig = plt.figure(figsize=(12, 6))
    m = Basemap(projection="cyl", resolution=quality)

    if background_name:
        img = plt.imread(background_name)
        m.imshow(img, origin="upper", extent=[-180, 180, -90, 90])

    m.drawparallels(np.arange(-90.0, 91.0, 30.0), labels=[1, 0, 0, 0], color="black")
    m.drawmeridians(np.arange(-180.0, 181.0, 30.0), labels=[0, 0, 0, 1], color="black")

    c_scheme = m.contourf(
        lon, lat, valid_data, cmap="coolwarm", extend="both", alpha=0.7
    )

    if (
        data_type == "Wind Speed(Direction)"
        and wind_data_ua is not None
        and wind_data_va is not None
    ):
        num = Arrows_switch(arrow_number, valid_data.shape[0])
        skip = valid_data.shape[0] // int(num)
        m.quiver(
            lon[::skip, ::skip],
            lat[::skip, ::skip],
            wind_data_ua[::skip, ::skip],
            wind_data_va[::skip, ::skip],
            scale=None,
        )

    cbar = m.colorbar(c_scheme, location="bottom", pad="10%")
    cbar.set_label(
        "Temperature (K)"
        if data_type == "Temperature"
        else "Pressure (Pa)" if data_type == "Pressure" else "Overall Wind Speed (m/s)"
    )
    plt.title(pic_name)
    plt.savefig(
        f"{file_path}/{pic_name.replace(' ', '_')}_{bg_type}.png",
        dpi=dpi,
        bbox_inches="tight",
    )


def Arrows_switch(arrow_number, secondData):
    return {
        "Few": secondData / 4,
        "Medium": secondData / 2,
        "Intensive": secondData,
    }.get(arrow_number)
