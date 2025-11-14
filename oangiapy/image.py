from PIL import Image
import numpy as np
import matplotlib.pyplot as plt
import cv2

def get_two_frames(video_path, frame_idx1, frame_idx2):
    """
    Extract two frames from a video as PIL Images.

    Args:
        video_path (str): Path to video file.
        frame_idx1 (int): Index of first frame (starting from 0).
        frame_idx2 (int): Index of second frame.

    Returns:
        tuple: (PIL.Image frame1, PIL.Image frame2)
    """
    cap = cv2.VideoCapture(video_path)
    frames = {}
    max_idx = max(frame_idx1, frame_idx2)
    current_idx = 0

    while current_idx <= max_idx:
        ret, frame = cap.read()
        if not ret:
            break  # end of video
        if current_idx == frame_idx1 or current_idx == frame_idx2:
            # Convert BGR to RGB
            frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frames[current_idx] = Image.fromarray(frame_rgb)
        current_idx += 1

    cap.release()

    f1 = frames.get(frame_idx1)
    f2 = frames.get(frame_idx2)
    if f1 is None or f2 is None:
        raise ValueError("One or both frame indices are out of range.")
    return f1, f2
def resize_and_crop(img, target_w, target_h):
    # Resize while keeping aspect ratio
    img_ratio = img.width / img.height
    target_ratio = target_w / target_h
    if img_ratio > target_ratio:
        # Wider → fit height
        new_height = target_h
        new_width = int(target_h * img_ratio)
    else:
        # Taller → fit width
        new_width = target_w
        new_height = int(target_w / img_ratio)

    img_resized = img.resize((new_width, new_height), Image.LANCZOS)

    # Center crop
    left = (new_width - target_w) // 2
    top = (new_height - target_h) // 2
    right = left + target_w
    bottom = top + target_h

    return img_resized.crop((left, top, right, bottom))

def process_images(img1, img2):
    img1 = Image.open(img1).convert("RGB")
    img2 = Image.open(img2).convert("RGB")
    w1, h1 = img1.size
    w2, h2 = img2.size

    # Determine target size (the smaller one)
    target_w = min(w1, w2)
    target_h = min(h1, h2)
    img1 = resize_and_crop(img1, target_w, target_h)
    img2 = resize_and_crop(img2, target_w, target_h)

    arr1 = np.array(img1, dtype=np.int32)
    arr2 = np.array(img2, dtype=np.int32)

    return img1, img2, arr1, arr2
# --- Step 1: Read two images and show them ---
def show_images(img1, img2):
    print("Step 1 - Image Info:")
    print(f" - Size: {img1.width} x {img1.height}")
    print(f" - Format: {img1.format}")
    print(f" - Mode: {img1.mode}")
    print("\n")
    print(f" - Size: {img2.width} x {img2.height}")
    print(f" - Format: {img2.format}")
    print(f" - Mode: {img2.mode}")
    print("\n")

    # Display both images
    plt.figure(figsize=(6,3))
    plt.subplot(1,2,1)
    plt.imshow(img1)
    plt.title(f"Original Image 1")
    plt.axis('off')

    plt.subplot(1,2,2)
    plt.imshow(img2)
    plt.title(f"Original Image 2")
    plt.axis('off')

    plt.show()

def count_differing_pixels(arr1, arr2, threshold_percent = 0):
    max_diff = np.sqrt(3 * 255**2)  # max Euclidean distance in RGB
    threshold = (threshold_percent / 100) * max_diff
    diff_mask = np.any(arr1 != arr2, axis=2)
    total_pixels = arr1.shape[0] * arr1.shape[1]

    # Compute Euclidean distance per pixel
    diff_sum = np.sum((arr1 - arr2) ** 2, axis=2)
    diff_magnitude = np.sqrt(diff_sum)

    # Pixels exceeding threshold
    diff_mask = diff_magnitude > threshold

    differing_pixels = np.sum(diff_mask)
    matching_pixels = total_pixels - differing_pixels
    diff_percent = (differing_pixels / total_pixels) * 100

    return matching_pixels, differing_pixels, diff_percent, diff_mask
# --- Step 2: Count differing pixels, show and save binary diff image ---

def differing_pixels(arr1, arr2, step = 1):
    print("Differing pixels")
    fig, axes = plt.subplots(3, 4)  # 2 rows, 6 columns
    thresholds = range(12)  # 0 to 11

    for idx, t in enumerate(thresholds):
        jump = t * step
        row = idx // 4
        col = idx % 4
        # Generate diff image
        matching_pixels, differing_pixels_count, diff_percent, diff_mask = count_differing_pixels(arr1, arr2, threshold_percent=jump)

        diff_image_arr = np.zeros((arr1.shape[0], arr1.shape[1], 3), dtype=np.uint8)
        diff_image_arr[~diff_mask] = [0, 255, 255]  # matches → cyan
        diff_image_arr[diff_mask] = [0, 0, 0]       # differences → black
        diff_image = Image.fromarray(diff_image_arr)

        axes[row, col].imshow(diff_image)
        axes[row, col].set_title(f"{jump}% - {diff_percent:.2f}%")
        axes[row, col].axis('off')

    plt.tight_layout()
    plt.show()
    #fig.savefig("pixel_difference_all_thresholds.png")
# --- Step 3: Per-pixel color difference, normalize, show and save ---
def visualize_color_difference(arr1, arr2, output_path):
    # Compute Euclidean distance per pixel
    diff_magnitude = np.sqrt(np.sum((arr1 - arr2)**2, axis=2))

    max_possible = np.sqrt(3 * 255**2)  # ~441.67
    total_pixels = arr1.shape[0] * arr1.shape[1]
    total_diff = np.sum(diff_magnitude)
    max_total_diff = max_possible * total_pixels
    total_diff_percent = (total_diff / max_total_diff) * 100
    #diff_magnitude = np.nan_to_num(diff_magnitude)
    # Compute percentage
    diff_percent = (diff_magnitude / max_possible) * 100

    print("Step 3 - Color Difference Magnitude:")
    print(f"- Max difference: {diff_magnitude.max():.2f} ({diff_percent.max():.2f}%)")
    print(f"- Min difference: {diff_magnitude.min():.2f} ({diff_percent.min():.2f}%)\n")
    print(f"- Total difference (sum of all pixels): {total_diff:.2f}")
    print(f"- Total difference percent: {total_diff_percent:.2f}%\n")
    # Grayscale image proportional to actual difference
    diff_image_arr = (diff_magnitude / max_possible * 255).astype(np.uint8)
    diff_image = Image.fromarray(diff_image_arr)
    diff_image.save(output_path)

    #plt.imshow(np.stack([diff_image_arr]*3, axis=-1) )
    #plt.title("Color Difference Magnitude (real)")
    #plt.axis('off')
    #plt.show()

# --- Main function ---
def analyze_images(img1_path, img2_path, output_path = "color_difference_map.png"):
    img1, img2, arr1, arr2 = process_images(img1_path, img2_path)
    #show_images(img1, img2)
    #differing_pixels(arr1, arr2, step = 1)
    #differing_pixels(arr1, arr2, step = 9)
    visualize_color_difference(arr1, arr2, output_path)

def images_to_video(input_folder, output_video, fps=30):
    """
    Convert a folder of images into a video.

    Args:
        input_folder (str): Folder containing sequential images (e.g., diff_00000.png, ...).
        output_video (str): Path for the output video (e.g., output.mp4).
        fps (int): Frames per second of the video.
    """
    # Get sorted list of images
    images = sorted(os.listdir(input_folder))
    images = [img for img in images if img.lower().endswith((".png", ".jpg", ".jpeg"))]

    if not images:
        print("No images found in folder.")
        return

    # Read the first image to get the size
    first_frame = cv2.imread(os.path.join(input_folder, images[0]))
    height, width, layers = first_frame.shape

    # Define the video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # for .mp4 output
    video = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

    for img_name in images:
        img_path = os.path.join(input_folder, img_name)
        frame = cv2.imread(img_path)
        video.write(frame)
        video.write(frame)
        video.write(frame)

    video.release()
    print(f"Video saved to {output_video}")
    
i1 = "IMG_0419.JPG"
i2 = "IMG_0419.webp"
i3 = "tam.jpg"
i4 = "i4.png"
i5 = "1.webp"
i6 = "2.webp"
analyze_images("frames/frame_00160.png", "frames/frame_00161.png")
#analyze_images("1.jpg", "2.jpg")



# Example usage
process_frame_pairs("frames", "diff_frames", analyze_images)

images_to_video("diff_frames", "diff_video.mp4", fps=30)