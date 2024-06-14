import math

def calculate_layer_heights(model_top, scale_factor, num_layers):
    heights = []
    for i in range(num_layers):
        if i == 0:
            layer_height = model_top / (
                math.pow(scale_factor, num_layers - 1)
                * (scale_factor - 1)
                / (scale_factor - 1)
            )
        else:
            layer_height = heights[i - 1] * scale_factor
        heights.append(layer_height)
    return heights


def output_layers(height, model_top, scale_factor, num_layers):
    heights = calculate_layer_heights(model_top, scale_factor, num_layers)

    for i in range(1, len(heights)):
        if heights[i - 1] <= height < heights[i]:
            return i

    if height < heights[0]:
        return 0

    return len(heights)