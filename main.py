from pathlib import Path
from tqdm import tqdm

from concurrent.futures import ProcessPoolExecutor, as_completed


import cv2


def process_image(input_path: Path, output_path: Path) -> None:
    """
    Image processing pipeline:
    - Remove left/right black border
    - Resize to 224x224

    Args:
        input_path (Path): Path to input image
        output_path (Path): Path to save processed image
    """

    # Read image
    img = cv2.imread(str(input_path))

    # Crop left/right black border
    border_width = 270
    img = img[:, border_width:-border_width, :]

    # Resize to fixed size
    target_size = 224
    img = cv2.resize(img, (target_size, target_size))

    # Save processed image
    cv2.imwrite(str(output_path), img)


# INPUT
img_paths = sorted(Path("images").glob("*.png"))

# OUTPUT
output_path = Path("output")
output_path.mkdir(exist_ok=True, parents=True)

# Multi process
with ProcessPoolExecutor(max_workers=15) as executor:
    for _ in tqdm(
        executor.map(
            process_image,
            img_paths,
            [output_path / img_path.name for img_path in img_paths],
        ),
        total=len(img_paths),
    ):
        pass
