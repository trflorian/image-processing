# Image Proceesing

A small image processing project exploring how to use multiprocessing to optimize a data procesisng pipeline by parallelizing a CPU bound task on multiple cores.

## Quickstart
To get started, simply clone the repo, make sure that you have uv installed and then snyc the project dependencies.
```
uv sync
```

Place some images in `./images/` folder or specify a custom input image directory with the `--input_path` argument. Then run the program, it will show a progress bar in the terminal indicating the progress and the iteration speed. 

```
uv run main.py
```

By default the program will run on a single core. If you specify e.g. `--num_workers 10` it will use a pool of 10 processes and parallelize the task across them. 

## Usage
```
usage: main.py [-h] [--input_path INPUT_PATH] [--output_path OUTPUT_PATH] [--image_extensions IMAGE_EXTENSIONS [IMAGE_EXTENSIONS ...]]
               [--num_workers NUM_WORKERS] [--timing] [--subset SUBSET]

options:
  -h, --help            show this help message and exit
  --input_path INPUT_PATH
                        Path to a folder with images
  --output_path OUTPUT_PATH
                        Path where the processed images will be stored
  --image_extensions IMAGE_EXTENSIONS [IMAGE_EXTENSIONS ...]
                        Extensions of image files to look for
  --num_workers NUM_WORKERS
                        Specify number of workers to use. If not specified, will use a single process for loop.
  --timing              Enable timing of the process and save results to a `timing.txt` file
  --subset SUBSET       Specify a subset of the images to process
```