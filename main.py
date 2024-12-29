import os
import time
import argparse

from pathlib import Path
from concurrent.futures import ProcessPoolExecutor

from tqdm import tqdm

import numpy as np
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


def run_single_process(input_paths: list[Path], output_paths: list[Path]) -> None:
    """
    Run the image processing on a single process

    Args:
        input_paths (list[Path]): List of all input image paths
        output_paths (list[Path]): List of output paths. Should have the same length as the input
    """
    for input_path, output_path in tqdm(
        zip(input_paths, output_paths), total=len(input_paths)
    ):
        process_image(
            input_path,
            output_path,
        )


def run_multi_process(
    num_processes: int, input_paths: list[Path], output_paths: list[Path]
) -> None:
    """
    Run the image processing on multiple processes.

    Args:
        num_processes (int): Number of parallel processes to use
        input_paths (list[Path]): List of all input image paths
        output_paths (list[Path]): List of output paths. Should have the same length as the input
    """
    with ProcessPoolExecutor(max_workers=num_processes) as executor:
        all_processes = executor.map(
            process_image,
            input_paths,
            output_paths,
        )
        for _ in tqdm(all_processes, total=len(input_paths)):
            pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--input_path",
        type=Path,
        default=Path("./images"),
        help="Path to a folder with images",
    )

    parser.add_argument(
        "--output_path",
        type=Path,
        default=Path("./output"),
        help="Path where the processed images will be stored",
    )

    parser.add_argument(
        "--image_extensions",
        type=str,
        nargs="+",
        default=["png", "jpg", "jpeg"],
        help="Extensions of image files to look for",
    )

    parser.add_argument(
        "--num_workers",
        type=int,
        default=None,
        help="Specify number of workers to use. If not specified, will use a single process for loop.",
    )

    parser.add_argument(
        "--timing",
        action="store_true",
        help="Enable timing of the process and save results to a `timing.txt` file",
    )

    parser.add_argument(
        "--subset",
        type=int,
        default=None,
        help="Specify a subset of the images to process",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()

    # INPUT
    input_paths = []
    for img_ext in args.image_extensions:
        input_paths += list(args.input_path.glob(f"*.{img_ext}"))
    input_paths = sorted(input_paths)

    subset = args.subset
    if subset:
        print(f"Using a subset of size {subset} for image processing!")
        input_paths = input_paths[:subset]

    # OUTPUT
    output_path = args.output_path
    output_path.mkdir(exist_ok=True, parents=True)
    output_paths = [output_path / img_path.name for img_path in input_paths]

    if not args.timing:
        # Not timing, just run image processing once
        num_workers = args.num_workers
        if num_workers is None:
            run_single_process(
                input_paths=input_paths,
                output_paths=output_paths,
            )
        else:
            run_multi_process(
                num_processes=num_workers,
                input_paths=input_paths,
                output_paths=output_paths,
            )
    else:
        timings = []

        for num_workers in range(1, os.process_cpu_count() + 20):
            st = time.perf_counter()
            run_multi_process(
                num_processes=num_workers,
                input_paths=input_paths,
                output_paths=output_paths,
            )
            et = time.perf_counter()
            dt = et - st
            timings.append([num_workers, dt])

        np.savetxt("timing.txt", timings, fmt="%.4f")
