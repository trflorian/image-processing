from pathlib import Path
from tqdm import tqdm

# INPUT
img_paths = Path("images").glob("*.png")

# OUTPUT
output_path = Path("output")
output_path.mkdir(exist_ok=True, parents=True)

for img_path in tqdm(sorted(img_paths)):
    pass