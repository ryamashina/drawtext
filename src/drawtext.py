#!/usr/bin/env python3

import pathlib
import argparse
from PIL import Image, ImageDraw, ImageFont


def main():
    parser = argparse.ArgumentParser(description="Draw text on JPEG.")
    parser.add_argument(
        'input_image_file', 
        help='File name of input image. The image must be in JPEG format.', 
        type=str,
    )
    parser.add_argument(
        'text', 
        help='Text for insert to image.', 
        type=str,
    )
    parser.add_argument(
        '-of',
        '--output_file',
        help='Output image file name. default is "${input_image_file}_drawtext.jpg".', 
        type=str,
    )
    parser.add_argument(
        '-ff',
        '--font_file',
        help='Font file name for text. default is "NotoSerifCJKjp-Black.otf".', 
        type=str,
    )
    parser.add_argument(
        '-fs',
        '--font_size',
        help='Font size for text. default is 50.', 
        type=int,
        default=50,
    )
    parser.add_argument(
        '-sw',
        '--stroke_width',
        help='Stroke width for text. default is 3.', 
        type=int,
        default=3,
    )
    parser.add_argument(
        '-sp',
        '--spacing',
        help='Spacing for text line. default is 0.', 
        type=int,
        default=0,
    )
    parser.add_argument(
        '-al',
        '--align',
        help='Align for text. default is "center".', 
        type=str,
        default="center",
    )
    parser.add_argument(
        '-fc',
        '--font_color',
        help='Font color for text. default is "#FFFF00".', 
        type=str,
        default="#FFFF00",
    )
    parser.add_argument(
        '-sc',
        '--stroke_color',
        help='Stroke color for text. default is "#000000".', 
        type=str,
        default="#000000",
    )
    parser.add_argument(
        '-rc',
        '--rect_color',
        help='Rect color for background of font. default is "#FFFFFF80".', 
        type=str,
        default="#FFFFFF80",
    )
    args = parser.parse_args()

    input_image_file = args.input_image_file
    text = args.text
    stroke_width = args.stroke_width
    spacing = args.spacing
    align = args.align
    font_color = args.font_color
    stroke_color = args.stroke_color
    rect_color = args.rect_color
    black_color = (0, 0, 0)
    yellow_color = (255, 255, 25)
    rect_fill_white_color = (255, 255, 255, 128)

    # set font
    font_file = args.font_file
    font_size = args.font_size
    if font_file is None:
        absolute_path = pathlib.Path(__file__).resolve()
        script_dir_path = absolute_path.parent
        font_file = str(
            script_dir_path.joinpath(
                "NotoSerifCJKjp-Black.otf",
            )
        )
    font = ImageFont.truetype(
        font_file,
        font_size,
    )

    # Declare output file name.
    output_file = args.output_file
    if output_file is None:
        p_file = pathlib.Path(input_image_file)
        p_dir = p_file.parent
        suffix = p_file.suffix
        stem = p_file.stem
        output_file = p_dir.joinpath(
            stem + "_drawtext" + suffix,
        )
        
    ## import image
    img = Image.open(input_image_file).copy()
    text_draw = ImageDraw.Draw(img)

    # get text_size
    text_size = text_draw.textsize(
        text,
        font=font,
        stroke_width=stroke_width,
        spacing=spacing,
    )

    # get text_position
    text_position_x = int(img.size[0] / 2 - text_size[0] / 2)
    text_position_y = int(img.size[1] / 2 - text_size[1] / 2)
    text_position = (text_position_x, text_position_y)

    # get rect position
    rect_position = (
        0,
        text_position[1],
        img.size[0],
        text_position[1] + text_size[1]
    )

    # draw rectangle
    img_alpha = img.convert('RGBA')
    rectangle_alpha = Image.new('RGBA', img.size)
    rectangle_draw = ImageDraw.Draw(rectangle_alpha)
    rectangle_draw.rectangle(rect_position, fill=rect_color)
    img = Image.alpha_composite(img_alpha, rectangle_alpha)
    img = img.convert("RGB")

    # draw text
    text_draw = ImageDraw.Draw(img)
    text_draw.text(
        text_position,
        text,
        font=font,
        fill=font_color,
        stroke_width=stroke_width,
        stroke_fill=stroke_color,
        align=align,
        spacing=spacing,
    )
    img.save(output_file)

if __name__ == "__main__":
    main()
