import numpy as np
import cv2
import matplotlib.pyplot as plt


def extract_physical_luminance(image_path):
    """ Task 1.1: Physical Luminance Extraction """
    img_bgr = cv2.imread(image_path)
    if img_bgr is None:
        raise ValueError(f"Image not found at path: {image_path}")

    # Resize for faster stochastic computation in portfolio demo
    img_bgr = cv2.resize(img_bgr, (640, 480))
    img_rgb = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2RGB)
    img_normalized = img_rgb.astype(np.float32) / 255.0

    R, G, B = img_normalized[:, :, 0], img_normalized[:, :, 1], img_normalized[:, :, 2]
    luminance_map = (0.2126 * R) + (0.7152 * G) + (0.0722 * B)
    return img_rgb, luminance_map


def apply_v1_gabor_filters(luminance_map):
    """ Task 1.2: V1 Biological Saliency """
    ksize, sigma, lambd, gamma, psi = 31, 4.0, 10.0, 0.5, 0
    orientations = [0, np.pi / 4, np.pi / 2, 3 * np.pi / 4]
    saliency_map = np.zeros_like(luminance_map)

    for theta in orientations:
        kernel = cv2.getGaborKernel((ksize, ksize), sigma, theta, lambd, gamma, psi, ktype=cv2.CV_32F)
        filtered_image = cv2.filter2D(luminance_map, cv2.CV_32F, kernel)
        saliency_map = np.maximum(saliency_map, np.abs(filtered_image))

    saliency_map = (saliency_map - np.min(saliency_map)) / (np.max(saliency_map) - np.min(saliency_map))
    return saliency_map


def simulate_stochastic_gaze(saliency_map, num_fixations=15):
    """
    Task 1.3: Stochastic Gaze Simulation (Markov Process)
    Simulates human saccades and fixations using a probability distribution
    weighted by both V1 saliency and spatial proximity (Gaussian penalty).
    """
    h, w = saliency_map.shape

    # Start the gaze at the center of the image (typical initial human bias)
    current_y, current_x = h // 2, w // 2
    trajectory = [(current_x, current_y)]

    # Create coordinate grids for spatial distance calculation
    x_grid, y_grid = np.meshgrid(np.arange(w), np.arange(h))

    for _ in range(num_fixations - 1):
        # 1. Spatial Penalty: Humans prefer shorter saccades.
        # We model this as a 2D Gaussian centered at the current gaze position.
        sigma_spatial = min(h, w) * 0.3  # Standard deviation for saccade distance
        spatial_gaussian = np.exp(-((x_grid - current_x) ** 2 + (y_grid - current_y) ** 2) / (2 * sigma_spatial ** 2))

        # 2. Transition Probability: Saliency * Spatial Proximity
        transition_prob = saliency_map * spatial_gaussian
        transition_prob = transition_prob / np.sum(transition_prob)  # Normalize to sum to 1

        # 3. Stochastic Jump (Markov Chain transition)
        flat_prob = transition_prob.flatten()
        next_index = np.random.choice(len(flat_prob), p=flat_prob)

        # Convert 1D index back to 2D coordinates
        current_y, current_x = divmod(next_index, w)
        trajectory.append((current_x, current_y))

    return trajectory


# Execution and visualization block
if __name__ == "__main__":
    sample_image = "sample.jpeg"

    try:
        # Pipeline Execution
        original_img, lum_map = extract_physical_luminance(sample_image)
        v1_saliency = apply_v1_gabor_filters(lum_map)
        gaze_trajectory = simulate_stochastic_gaze(v1_saliency, num_fixations=20)

        # Plotting the Gaze Trajectory
        fig, ax = plt.subplots(1, 3, figsize=(18, 5))

        ax[0].imshow(original_img)
        ax[0].set_title("1. Original Scene (RGB)")
        ax[0].axis('off')

        ax[1].imshow(v1_saliency, cmap='inferno')
        ax[1].set_title("2. V1 Saliency Map")
        ax[1].axis('off')

        # Draw trajectory on the original image
        ax[2].imshow(original_img)
        ax[2].set_title("3. Simulated Gaze Trajectory")
        ax[2].axis('off')

        # Plot fixations (dots) and saccades (lines)
        x_coords, y_coords = zip(*gaze_trajectory)
        ax[2].plot(x_coords, y_coords, color='cyan', linewidth=2, alpha=0.7, label='Saccades')
        ax[2].scatter(x_coords, y_coords, color='red', s=50, zorder=5, label='Fixations')
        ax[2].scatter(x_coords[0], y_coords[0], color='yellow', s=100, marker='*', zorder=10, label='Start Point')
        ax[2].legend(loc='upper right')

        plt.tight_layout()
        plt.show()

    except Exception as e:
        print(f"Error: {e}")