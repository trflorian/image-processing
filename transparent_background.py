import numpy as np
import cv2


def background_blended(
    img: np.ndarray, bg_color: tuple = (255, 255, 255), bg_padding: int = 20
) -> np.ndarray:
    """
    Blends an image with an alpha channel onto a white background.

    Args:
        img (np.ndarray): Image with an alpha channel.
        bg_color (tuple): Background color in BGR format.
        bg_padding (int): Padding around the image.
    
    Returns:
        np.ndarray: Image with the alpha channel blended onto a white background.
    """
    # Make sure to not modify the original image
    img = img.copy()

    # Split the image into B, G, R, and Alpha channels
    img_bgr_original = img[:, :, :3].astype(float)
    alpha = img[:, :, 3].astype(np.uint8)
    print("Image has an alpha channel. Proceeding to blend with white background.")

    # Normalize the alpha channel to range [0, 1]
    alpha = alpha / 255.0

    # Create a white background
    img_bgr_background = np.full_like(
        a=img_bgr_original, fill_value=bg_color, dtype=float
    )

    print(f"{img.shape=}") # img.shape=(69, 244, 4)
    print(f"{img_bgr_original.shape=}") # img_bgr_original.shape=(69, 244, 3)
    print(f"{img_bgr_background.shape=}") # img_bgr_background.shape=(69, 244, 3)
    print(f"{alpha.shape=}") # alpha.shape=(69, 244)

    alpha = np.expand_dims(alpha, axis=-1)

    print(f"{alpha.shape=}") # alpha.shape=(69, 244, 1)

    # Blend the color image with the white background using the alpha mask
    img_blended = alpha * img_bgr_original + (1 - alpha) * img_bgr_background
    img_blended = img_blended.astype(np.uint8)

    # Add padding around the image
    img_blended = cv2.copyMakeBorder(
        img_blended, bg_padding, bg_padding, bg_padding, bg_padding, cv2.BORDER_CONSTANT, value=bg_color
    )

    return img_blended


def background_binary(
    img: np.ndarray, bg_threshold: int = 80, bg_color: tuple = (255, 255, 255)
) -> np.ndarray:
    """
    Replaces the background of an image with a given color based on a binary threshold.

    Args:
        img (np.ndarray): Image with an alpha channel.
        threshold (int): Threshold value for the alpha channel.
        bg_color (tuple): Background color in BGR format.
    
    Returns:
        np.ndarray: Image with the background replaced by the given color.
    """
    # Make sure to not modify the original image
    img = img.copy()

    # Threshold alpha channel
    bg_indices = img[:, :, 3] <= bg_threshold

    # Replace image at indices with background color
    img[bg_indices, :3] = bg_color

    return img


if __name__ == "__main__":
    img = cv2.imread("images/equation.png", flags=cv2.IMREAD_UNCHANGED)

    # add light orange background, BGR
    # col = (255, 255, 255) # White
    col = (200, 220, 255) # Orange

    # Binary Background
    img_bg_binary = background_binary(img, bg_color=col,bg_threshold=80)

    # Blended Background
    img_bg_blended = background_blended(img, bg_color=col, bg_padding=20)

    cv2.imshow("Image", img)
    cv2.imshow("Binary Background", img_bg_binary)
    cv2.imshow("Blended Background", img_bg_blended)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
