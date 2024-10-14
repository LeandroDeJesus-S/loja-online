import os
import pytest
from PIL import Image
from tempfile import tempdir

from utils.support.func import resize_image

params = [
    # real_size, max_dim, expected_dim
    ((100, 100), (100, 100), (100, 100)),
    ((100, 100), (50, 100), (50, 100)),
    ((100, 100), (100, 50), (100, 50)),
    ((100, 100), (50, 50), (50, 50)),
    ((100, 100), (25, None), (25, 25)),
]
@pytest.mark.parametrize('real_size,max_dim,expected_dim', params)
def test_resize_image_success(real_size, max_dim, expected_dim):
    """test if the resize_image func is working as well.

    Args:
        real_size (tuple): the original dimension of the image.
        max_dim (tuple): the max dimension to the image.
        expected_dim (tuple): the final dimension expected after to resize.
    """
    image = Image.new('RGB', real_size, color='white')
    img_path = os.path.join(str(tempdir), 'temp_img.jpeg')
    try:
        image.save(img_path)

        resize_image(img_path, *max_dim)

        resized_image = Image.open(img_path)
        new_size = resized_image.size
        assert new_size == expected_dim

    finally:
        if os.path.exists(img_path):
            os.remove(img_path)
