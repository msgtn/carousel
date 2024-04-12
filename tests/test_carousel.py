import glob
import pytest
import carousel
from PIL import Image

IMAGE_SIZE = (1080, 1354)
SOURCE_DIR = '../240331_nyc_mpi/*'
CONCAT_IMAGE_PATH = './concat_image.jpg'

class TestCarousel():

    @pytest.mark.parametrize('image_paths', [sorted(glob.glob(SOURCE_DIR))])
    def test_concatenate(self, image_paths):
        images = [Image.open(image) for image in image_paths]
        concatenated_image = carousel.concatenate(
            images,
            height=IMAGE_SIZE[1],
        )
        concatenated_image.save(CONCAT_IMAGE_PATH)
        # breakpoint()

    @pytest.mark.parametrize('image_path', [CONCAT_IMAGE_PATH])
    def test_split(self, image_path):
        image = Image.open(image_path)
        split_images = carousel.split(
            image, aspect_ratio=4/5
        )
        for i,image in enumerate(split_images):
            image.save(f"./split{i}.jpg")