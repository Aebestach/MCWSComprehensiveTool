from PIL import Image, ImageDraw
import numpy as np
from scipy.ndimage import binary_dilation
import imageio
import os

def handle_KSP(file_path):
    base_name = os.path.basename(file_path)
    file_name_without_extension, _ = os.path.splitext(base_name)
    if file_path.endswith(".dds"):
        dds_image = imageio.imread(file_path)
        img = Image.fromarray(dds_image)
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
    else:
        img = Image.open(file_path)
        img = img.transpose(Image.FLIP_LEFT_RIGHT)

    width, height = img.size
    quarter_width = width // 4 if file_path.endswith(".dds") else width // 4

    quarters = (
        [
            img.crop((quarter_width * i, 0, quarter_width * (i + 1), height))
            for i in range(4)
        ]
        if file_path.endswith(".dds")
        else [
            img.crop((quarter_width * i, 0, quarter_width * (i + 1), height))
            for i in range(4)
        ]
    )
    quarters = quarters[1:] + [quarters[0]]

    final_img = Image.new("RGBA", (width, height))
    for i, quarter in enumerate(quarters):
        final_img.paste(
            quarter,
            (
                (quarter_width * i, 0)
                if file_path.endswith(".dds")
                else (quarter_width * i, 0)
            ),
        )
    final_img.save(file_name_without_extension+".png", compress_level=1)


def handle_ExoPlaSim(file_path):
    if file_path.endswith(".dds"):
        dds_image = imageio.imread(file_path)
        img = Image.fromarray(dds_image)
        img = img.transpose(Image.FLIP_TOP_BOTTOM)
    else:
        img = Image.open(file_path)
        img = img.transpose(Image.FLIP_LEFT_RIGHT)

    width, height = img.size
    quarter_width = width // 4

    quarters = [
        img.crop((quarter_width * i, 0, quarter_width * (i + 1), height))
        for i in range(4)
    ]
    quarters = [quarters[-1]] + quarters[:-1]

    final_img = Image.new("RGBA", (width, height))
    for i, quarter in enumerate(quarters):
        final_img.paste(
            quarter,
            (quarter_width * i, 0),
        )

    final_img.save("height_map.png", compress_level=1)


def handle_coatline(file_path):
    img = Image.open(file_path).convert("RGBA")
    alpha_channel = img.split()[-1]
    alpha_array = np.array(alpha_channel)

    line_thickness = 5

    output_img = Image.new("RGBA", img.size)
    draw = ImageDraw.Draw(output_img)

    land_mask = alpha_array > 0
    edge_mask = land_mask ^ binary_dilation(land_mask, iterations=line_thickness)

    y, x = np.where(edge_mask)
    for i, j in zip(y, x):
        draw.ellipse(
            (
                j - line_thickness,
                i - line_thickness,
                j + line_thickness,
                i + line_thickness,
            ),
            fill="black",
        )

    output_img.save("coastline.png")
    handle_KSP("coastline.png")
