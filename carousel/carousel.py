import glob
import os
import pathlib
import sys
from PIL import Image
import argparse


def concatenate(images, height=float("inf")):
    """
    Concatenate images.

    :param images: _description_
    """

    sizes, aspect_ratios, heights, widths = [], [], [], []
    resized_images = []
    total_width = 0
    for image in images:
        size = image.size
        sizes.append(size)
        widths.append(size[0])
        heights.append(size[1])
        aspect_ratios.append(size[0] / size[1])
        total_width += size[0]
        height = min(height, size[1])

    canvas = Image.new(mode="RGBA", size=(total_width, height), color=(255, 255, 255))

    # current x-position to place the image
    # always y-position = 0
    x = 0
    for image, aspect_ratio in zip(images, aspect_ratios):
        new_width = int(aspect_ratio * height)
        resized_image = image.resize(size=(new_width, height))
        resized_image.putalpha(255)
        canvas.alpha_composite(resized_image, dest=(x, 0))
        x += new_width

    canvas = canvas.crop(box=(0, 0, x, height))
    canvas = canvas.convert("RGB")
    return canvas
    # return image


def split(image, num_panels=None, aspect_ratio=None):
    """
    Splits an image by EITHER number of panels or an aspect ratio

    """
    if aspect_ratio:
        width, height = image.size
        panel_width = int(height * aspect_ratio)

        images = []
        x = 0
        while x <= width:
            images.append(image.crop((x, 0, x + panel_width, height)))
            x += panel_width

    return images


def main():
    if len(sys.argv) < 2:
        print("Usage: python carousel.py <image_dir>")
        sys.exit(1)
    image_dir = pathlib.Path(sys.argv[1]).resolve()
    collection_name = os.path.basename(image_dir)
    splits_dir = image_dir / f"{collection_name}_splits"
    os.makedirs(splits_dir, exist_ok=True)

    image_paths = sorted(glob.glob(str(image_dir / "*.jpg")))
    images = [Image.open(image) for image in image_paths]
    IMAGE_SIZE = images[0].size
    concatenated_image = concatenate(
        images,
        height=IMAGE_SIZE[1],
    )
    split_images = split(concatenated_image, aspect_ratio=4 / 5)
    for i, image in enumerate(split_images):
        image.save(str(splits_dir / f"{collection_name}_split{i}.jpg"))


if __name__ == "__main__":
    main()
