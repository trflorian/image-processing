from pathlib import Path
from tqdm import tqdm

from concurrent.futures import ProcessPoolExecutor

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


if __name__ == "__main__":
    # INPUT
    img_paths = sorted(Path("images").glob("*.png"))[:1000]

    # OUTPUT
    output_path = Path("output")
    output_path.mkdir(exist_ok=True, parents=True)

    # # Single Process
    # for img_path in tqdm(img_paths):
    #     process_image(
    #         input_path=img_path,
    #         output_path=output_path / img_path.name,
    #     )

    # Multi process

    output_paths = [output_path / img_path.name for img_path in img_paths]

    import time

    import numpy as np

    timing = []

    for num_workers in range(1, 61):
        st = time.perf_counter()
        with ProcessPoolExecutor(num_workers) as executor:
            all_processes = executor.map(
                process_image,
                img_paths,
                output_paths,
            )
            for _ in tqdm(all_processes, total=len(img_paths)):
                pass
        et = time.perf_counter()
        dt = et - st
        print(num_workers, dt)
        timing.append([num_workers, dt])

    np.savetxt("timing.txt", timing, fmt="%.4f")
