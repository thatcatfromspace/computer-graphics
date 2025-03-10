import matplotlib.pyplot as plt
from PIL import Image
import cv2
import numpy
from scipy import ndimage
from skimage.morphology import skeletonize

class ImageUtils:
    def show_image(self, img_path: str):
        try:
            image = Image.open(img_path)
            plt.imshow(image)
            plt.show()
        except FileNotFoundError:
            print("File not found.")

    def create_image(self):
        image = Image.new("RGBA",(1000,600),color = (128, 128, 0, 1))
        plt.imshow(image)
        plt.show()

    def rotate_image(self, img_path: str, angle: int, resize: bool = False, fill_color: int | tuple[int] = 0):
        try:
            image = Image.open(img_path)
            image = image.rotate(angle, expand=resize, fillcolor=fill_color)
            plt.imshow(image)
            plt.show()
        except FileNotFoundError:
            print("File not found.")

    def show_image_metadata(self, img_path):
        try:
            image = Image.open(img_path)
            print(image.size)
            print(image.filename)
            print(image.format)
            print(image.format_description)
        except FileNotFoundError:
            print("File not found.")

    def resize_image(self, img_path: str, resize: tuple[int, int]):
        try:
            image = Image.open(img_path)
            image = image.resize(resize)
            plt.imshow(image)
            plt.show()
        except FileNotFoundError:
            print("File not found.")

    def quantize_image(self, img_path: str, quantised_colors: int = 8):
        try:
            image = Image.open(img_path)
            q_image = image.quantize(quantised_colors)
            fig, ax = plt.subplots(1, 2)
            ax[0].imshow(image)
            ax[0].set_title("Original image")

            ax[1].imshow(q_image)
            ax[1].set_title("Quantized image")

            plt.show()
        except FileNotFoundError:
            print("File not found.")

    def image_from_random(self, dim_xy: tuple[int, int] = (200, 200), file_path: str = "image.png"):
        img_arr = numpy.zeros((dim_xy[0], dim_xy[1]))
        for r in range(dim_xy[0]):
            for c in range(dim_xy[1]):
                img_arr[r, c] = numpy.random.randint(0, 2)

        cv2.imwrite(file_path, img_arr)

        image = Image.open(file_path)
        plt.imshow(image, cmap='grey')
        plt.show()

    def generate_histogram(self, img_path: str):
        image = cv2.imread(img_path)
        gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY) # convert to gray levels before plotting histogram

        plt.hist(gray_image.ravel(), bins=256, range=[0, 256]) # ravel() flattens into 1D array
        plt.show()

    def equalize_histogram(self, img_path: str):
        image = cv2.imread(img_path)
        gray_image = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
        equalized_image = cv2.equalizeHist(gray_image)

        fig, ax = plt.subplots(2, 2)

        ax[0, 0].imshow(gray_image, cmap='grey')
        ax[0, 0].set_title("Original image (grayscale)")
        ax[0, 1].imshow(equalized_image, cmap='grey')
        ax[0, 1].set_title("Equalized image")

        og_hist, og_bins = numpy.histogram(gray_image.ravel(), bins=256, range=[0, 256])
        eq_hist, eq_bins = numpy.histogram(equalized_image.ravel(), bins=256, range=[0, 256])

        ax[1, 0].plot(og_bins[:-1], og_hist)
        ax[1, 1].plot(eq_bins[:-1], eq_hist)

        ax[1, 0].plot(og_hist)
        ax[1, 1].plot(eq_hist)

        plt.show()

class Padding:
    def zero_padding(self, img_pth: str, pad: int):
        image = cv2.imread(img_pth)
        padding = numpy.pad(image, ((pad, pad), (pad, pad), (0, 0)), 'constant', constant_values=(0, 0))
        padded_image = Image.fromarray(padding)
        plt.imshow(padded_image, cmap='grey')
        plt.show()

    def constant_padding(self, img_pth: str, pad: int):
        image = cv2.imread(img_pth)
        padding = numpy.pad(image, ((pad, pad), (pad, pad), (0, 0)), 'constant', constant_values=(255, 255))
        padded_image = Image.fromarray(padding)
        plt.imshow(padded_image, cmap='grey')
        plt.show()

    def nearest_neighbour_padding(self, img_pth: str, pad: int):
        image = cv2.imread(img_pth)
        padding = numpy.pad(image, ((pad, pad), (pad, pad), (0, 0)), 'edge') # ((top, bottom), (left, right), (0, 0)), 3rd tuple is zero because no change in depth
                                                                            # 'edge' is the mode for nearest neighbour padding 
        padded_image = Image.fromarray(padding)
        plt.imshow(padded_image, cmap='grey')
        plt.show()


    def reflect_padding(self, img_pth: str, pad: int):
        image = cv2.imread(img_pth)
        padding = numpy.pad(image, ((pad, pad), (pad, pad), (0, 0)), 'reflect')
        padded_image = Image.fromarray(padding)
        plt.imshow(padded_image, cmap='grey')
        plt.show()

class Filters():
    def _correct_display_image(self, original_img: Image, filtered_img: Image):
        actual_corrected_image = cv2.cvtColor(original_img, cv2.COLOR_BGR2RGB)
        original_img = Image.fromarray(actual_corrected_image)
        
        filtered_corrected_image = cv2.cvtColor(filtered_img, cv2.COLOR_BGR2RGB)
        filtered_img = Image.fromarray(filtered_corrected_image)
        
        fig, ax = plt.subplots(1, 2)
        ax[0].imshow(original_img, cmap='grey')
        ax[0].set_title("Original image")
        ax[1].imshow(filtered_img, cmap='grey')
        ax[1].set_title("Filtered image")
        
        plt.show()

    def mean_filter(self, img_pth: str, kernel_size: int):
        '''
        Purpose: The mean filter aims to smooth images, reducing noise and minor variations in intensity.

        How It Works: This linear filter replaces each pixel's value with the average value of its neighboring pixels within a defined kernel (e.g., 3x3, 5x5). By averaging the intensities, the filter softens sharp transitions, leading to a blurred effect.
        '''
        image = cv2.imread(img_pth)
        kernel = numpy.ones((kernel_size, kernel_size), numpy.float32) / (kernel_size * kernel_size)
        filtered_image = cv2.filter2D(image, -1, kernel)

        self._correct_display_image(image, filtered_image)
            

    def median_filter(self, img_pth: str, kernel_size: int):
        '''
        Purpose: The median filter is designed to remove impulse noise while preserving edges.

        How It Works: This nonlinear filter sorts the pixel values within a neighborhood defined by the kernel and replaces the central pixel with the median value of the sorted list. This process effectively removes outliers without blurring edges.
        '''
        # kernel size should always be odd
        image = cv2.imread(img_pth)
        filtered_image = cv2.medianBlur(image, kernel_size)
        
        self._correct_display_image(image, filtered_image)

    def max_filter(self, img_pth: str, kernel_size: int):
        '''
        *Purpose*: The maximum filter enhances bright regions and reduces pepper noise (dark spots).

        *How It Works*: This filter examines the pixel values within the kernel and replaces the central pixel with the maximum value found. This operation causes bright areas to expand, effectively filling in small dark holes.
    
        Note: The maximum filter is a morphological operation known as dilation.
        '''
        image = cv2.imread(img_pth)
        kernel = numpy.ones((kernel_size, kernel_size), numpy.float32)
        filtered_image = cv2.dilate(image, kernel)

        self._correct_display_image(image, filtered_image)

    def min_filter(self, img_pth: str, kernel_size: int):
        '''
        *Purpose*: The minimum filter emphasizes dark regions and reduces salt noise (bright spots).

        *How It Works*: This filter scans the neighborhood defined by the kernel and assigns the minimum pixel value to the central pixel. This process causes dark areas to grow, eroding small bright spots.

        Note: The minimum filter is a morphological operation known as erosion.
        '''
        image = cv2.imread(img_pth)
        kernel = numpy.ones((kernel_size, kernel_size), numpy.float32)
        filtered_image = cv2.erode(image, kernel)

        self._correct_display_image(image, filtered_image)
    

class EdgeDetection:    
    '''
    In OpenCV, the `ddepth` parameter specifies the desired depth (data type) of the output image when applying image processing operations, such as filtering. The depth of an image refers to the number of bits used to represent each pixel's intensity value, determining the range of possible values.

    **Common `ddepth` Constants:**

    OpenCV defines several constants to represent different image depths:

    - `CV_8U`: 8-bit unsigned integers (0 to 255)
    - `CV_16U`: 16-bit unsigned integers (0 to 65,535)
    - `CV_16S`: 16-bit signed integers (−32,768 to 32,767)
    - `CV_32F`: 32-bit floating-point numbers
    - `CV_64F`: 64-bit floating-point numbers

    **Usage of `ddepth`:**

    The choice of `ddepth` affects how pixel values are stored and can influence the outcome of image processing operations. Selecting an appropriate depth is crucial to prevent issues like overflow or underflow, especially when performing operations that can produce values outside the original data type's range.

    **Special Case: `ddepth = -1`**

    Setting `ddepth` to `-1` indicates that the output image will have the same depth as the source image. This is useful when you want to maintain consistency in data types between the inumpyut and output images.
    '''
    def sobel_detection(self, img_pth: str, kernel_size: int = 3):
        '''
        Sobel edge detection is good for edge detection because it uses two different kernels thus it can detect edges in both the horizontal and vertical phases.2
        '''
        # lower kernel size detects most edges
        image = cv2.imread(img_pth)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        sobel_x = cv2.Sobel(gray_image, cv2.CV_64F, 1, 0, ksize=kernel_size)
        sobel_y = cv2.Sobel(gray_image, cv2.CV_64F, 0, 1, ksize=kernel_size)

        magnitude = numpy.sqrt(sobel_x**2 + sobel_y**2)

        # normalize to 0 to 255
        magnitude = numpy.uint8(255 * magnitude / numpy.max(magnitude))

        fig, ax = plt.subplots(4, 1)
        ax[0].imshow(gray_image, cmap='gray')
        ax[0].set_title("Original image")
        ax[1].imshow(sobel_x, cmap='gray')
        ax[1].set_title("Sobel X")
        ax[2].imshow(sobel_y, cmap='gray')
        ax[2].set_title("Sobel Y")
        ax[3].imshow(magnitude, cmap='gray')
        ax[3].set_title("Sobel magnitude")

        plt.show()

    def canny_detection(self, img_pth: str, thresholds: tuple[int, int] = (100, 200)):
        '''
        Uses two thresholds, high and low to eliminate ambiguity, in that it detects strong edges and weak edges within an image improving on the algorithm's robustness.
        '''
        image = cv2.imread(img_pth)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(gray_image, *thresholds)

        fig, ax = plt.subplots(1, 2)
        ax[0].imshow(gray_image, cmap='gray')
        ax[0].set_title("Original image")
        ax[1].imshow(edges, cmap='gray')
        ax[1].set_title("Canny edge detection")

        plt.show()

    def prewitt_detection(self, img_pth: str, kernel_size: int = 3):
        '''
        Prewitt edge detection is similar to Sobel edge detection but uses a different kernel.
        '''
        image = cv2.imread(img_pth)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        prewitt_x = cv2.filter2D(gray_image, -1, numpy.array([[-1, 0, 1], [-1, 0, 1], [-1, 0, 1]]))
        prewitt_y = cv2.filter2D(gray_image, -1, numpy.array([[-1, -1, -1], [0, 0, 0], [1, 1, 1]]))

        fig, ax = plt.subplots(4, 1)
        ax[0].imshow(gray_image, cmap='gray')
        ax[0].set_title("Original image")
        ax[1].imshow(prewitt_x, cmap='gray')
        ax[1].set_title("Prewitt X")
        ax[2].imshow(prewitt_y, cmap='gray')
        ax[2].set_title("Prewitt Y")
        ax[3].imshow(prewitt_x + prewitt_y, cmap='gray')
        ax[3].set_title("Prewitt magnitude")

        plt.show()

    def laplacian(self, img_pth: str, kernel_size: int = 3):
        '''
        The Laplacian edge detection is used to detect edges in an image using a single kernel.
        '''
        image = cv2.imread(img_pth)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        laplacian = cv2.Laplacian(gray_image, cv2.CV_64F, ksize=kernel_size)

        fig, ax = plt.subplots(2, 1)
        ax[0].imshow(gray_image, cmap='gray')
        ax[0].set_title("Original image")
        ax[1].imshow(laplacian, cmap='gray')
        ax[1].set_title("Laplacian edge detection")

        plt.show()

    def laplacian_of_gaussian(self, img_pth: str, kernel_size: int = 3):
        '''
        Modification of the Laplacian edge detection algorithm.
        '''
        image = cv2.imread(img_pth)
        gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        log_image = ndimage.gaussian_laplace(gray_image, sigma=kernel_size)
        

        fig, ax = plt.subplots(2, 1)
        ax[0].imshow(gray_image, cmap='gray')
        ax[0].set_title("Original image")
        ax[1].imshow(log_image, cmap='gray')
        ax[1].set_title("Laplacian of Gaussian edge detection")

        plt.show()

class ImageEnhancement:
    def power_law_transformation(self, img_pth: str, gamma: float):
        '''
        Power law transformation is a type of image enhancement technique that applies a power function to intensify the pixel values in an image. This transformation is also known as gamma correction or gamma adjustment.
        '''
        image = cv2.imread(img_pth)
        gamma_corrected = numpy.array(255 * (image / 255) ** gamma, dtype='uint8')

        fig, ax = plt.subplots(1, 2)
        ax[0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        ax[0].set_title("Original image")
        ax[1].imshow(cv2.cvtColor(gamma_corrected, cv2.COLOR_BGR2RGB))
        ax[1].set_title("Gamma corrected image")

        plt.show()

    def log_transformation(self, img_pth: str):
        '''
        Logarithmic transformation is a type of image enhancement technique that applies a logarithmic function to increase the pixel values in an image. This transformation is useful for expanding the dynamic range of images with low contrast.
        '''
        image = cv2.imread(img_pth)
        c = 255 / numpy.log(1 + numpy.max(image))
        log_corrected = numpy.array(c * numpy.log(1 + image), dtype='uint8')

        fig, ax = plt.subplots(1, 2)
        ax[0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        ax[0].set_title("Original image")
        ax[1].imshow(cv2.cvtColor(log_corrected, cv2.COLOR_BGR2RGB))
        ax[1].set_title("Log corrected image")

        plt.show()


class MorphologicalOperations:
    '''
    For dilation, erosion and their greyscale counterparts, see `Filters`.
    '''
    def opening_closing(self, img_pth: str, kernel_size: int):
        '''
        Opening and closing are morphological operations used to remove noise and small objects from images.

        Opening: This operation performs erosion followed by dilation, removing small objects and smoothing boundaries.
        Closing: This operation performs dilation followed by erosion, filling small holes and smoothing boundaries.
        '''
        image = cv2.imread(img_pth)
        kernel = numpy.ones((kernel_size, kernel_size), numpy.uint8)
        opening = cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
        closing = cv2.morphologyEx(image, cv2.MORPH_CLOSE, kernel)

        fig, ax = plt.subplots(1, 3)
        ax[0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        ax[0].set_title("Original image")
        ax[1].imshow(cv2.cvtColor(opening, cv2.COLOR_BGR2RGB))
        ax[1].set_title("Opening")
        ax[2].imshow(cv2.cvtColor(closing, cv2.COLOR_BGR2RGB))
        ax[2].set_title("Closing")

        plt.show()

    def hit_or_miss(self, img_pth: str):
        '''
        The hit-or-miss transform is a morphological operation used for pattern matching in binary images. It identifies the locations of specific shapes or structures within an image by detecting the presence of a pattern and its complement.

        The hit-or-miss transform is particularly useful for detecting objects with specific configurations, such as corners, T-junctions, or other geometric shapes. By defining a pair of structuring elements—one for the pattern and one for its complement—the operation can locate these structures within the image.
        '''
        img = cv2.imread(img_pth, cv2.IMREAD_GRAYSCALE)
        _, binary_image = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY) # ensure that image is binary
        kernel = numpy.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], numpy.uint8) # kernel is the pattern needed to be detected
        hit_or_miss = cv2.morphologyEx(img, cv2.MORPH_HITMISS, kernel)
        
        fig, ax = plt.subplots(1, 2)
        ax[0].imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        ax[0].set_title("Original image")
        ax[1].imshow(cv2.cvtColor(hit_or_miss, cv2.COLOR_BGR2RGB))
        ax[1].set_title("Hit or miss")

        plt.show()

    def thicken(self, img_pth: str):
        image = cv2.imread(img_pth, cv2.IMREAD_GRAYSCALE)
        _, binary_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

        # invert
        binary_image = binary_image == 0
        skeleton = skeletonize(binary_image)

        # invert back
        skeleton = numpy.invert(skeleton)

        plt.imshow(skeleton, cmap='gray')
        plt.show()

    def thin(self, img_pth: str, kernel_size: tuple[int, int] = (3, 3)):
        image = cv2.imread(img_pth, cv2.IMREAD_GRAYSCALE)
        _, binary_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)

        kernel = numpy.ones(kernel_size, numpy.uint8)   

        thinned_image = cv2.dilate(binary_image, kernel)

        plt.imshow(thinned_image, cmap='gray')
        plt.show()

    def skeletonize_image(self, img_path: str):
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)

        _, bin_img = cv2.threshold(img, 125, 255, cv2.THRESH_BINARY)

        skeleton = skeletonize(bin_img)

        skeleton = numpy.invert(skeleton)

        plt.imshow(skeleton, cmap='grey')
        plt.show()


class Convolutions:
    def ideal_lowpass_filter(self, image_path: str, cutoff_frequency: int):
        '''
        Ideal lowpasss filters need to performed in frequency domain because of the ability to specify
        a precise cutoff frequency. In spatial domains, infinite impulses make it extremely hard
        to perform lowpass filtering.
        '''
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        if image is None:
            print("Error: Image not found or unable to load.")
            return

        # Get image dimensions
        rows, cols = image.shape
        crow, ccol = rows // 2 , cols // 2  # center

        # Perform FFT
        dft = numpy.fft.fft2(image)
        dft_shift = numpy.fft.fftshift(dft)

        # Create a mask with a central square of 1s and the rest will be 0s
        mask = numpy.zeros((rows, cols), numpy.uint8)
        mask[crow - cutoff_frequency:crow + cutoff_frequency, ccol - cutoff_frequency:ccol + cutoff_frequency] = 1

        # Apply mask to the shifted DFT
        fshift = dft_shift * mask

        # Inverse FFT to get the image back
        f_ishift = numpy.fft.ifftshift(fshift)
        img_back = numpy.fft.ifft2(f_ishift)
        img_back = numpy.abs(img_back)

        # Display the results
        _, ax = plt.subplots(1, 2)
        ax[0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        ax[1].imshow(img_back, cmap='grey')

        plt.show()

    def gaussian_lowpass_filter(self, img_path: str, kernel: int = 2):
        image = cv2.imread(img_path)
        gaussian = ndimage.gaussian_filter(image, kernel) 

        _, ax = plt.subplots(1, 2)

        ax[0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY), cmap='grey')
        ax[0].set_title("Image")
        ax[0].axis('off')
        ax[1].imshow(gaussian)
        ax[1].set_title("Gaussian blur")
        ax[1].axis('off')

        plt.show()


    def gaussian_highpass_filter(self, img_path: str, kernel: int = 2):
        image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        gaussian = ndimage.gaussian_filter(image, kernel) 

        high_pass = image - gaussian
        high_pass_norm = cv2.normalize(high_pass, None, 0, 255, cv2.NORM_MINMAX)
        high_pass_norm = high_pass_norm.astype(numpy.uint8)

        _, ax = plt.subplots(1, 2)

        ax[0].imshow(image, cmap='grey')
        ax[0].set_title("Image")
        ax[0].axis('off')
        ax[1].imshow(cv2.cvtColor(high_pass_norm, cv2.COLOR_GRAY2RGB))
        ax[1].set_title("Gaussian blur")
        ax[1].axis('off')

        plt.show()


class Segmentation:
    def histogram_segmentation(self, image_path: str, bins: int = 60):
        '''
        Uses Otsu's method (a popular histogram-based thresholding approach).
        It computes the threshold that minimizes intra-class variance.
        '''
        image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

        image_smooth = ndimage.gaussian_filter(image, sigma=2)
        
        hist, bin_edges = numpy.histogram(image_smooth, bins=bins, range=(0, 256))
        # The expression bin_edges[:-1] takes all elements of the bin_edges array except the last one, 
        # while bin_edges[1:] takes all elements except the first one. By adding these two arrays element-wise 
        # and multiplying by 0.5, the code effectively computes the midpoint for each bin.
        bin_centers = 0.5 * (bin_edges[:-1] + bin_edges[1:])
        
        ret, segmented = cv2.threshold(image_smooth, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        print("Otsu threshold value:", ret)
        
        fig, ax = plt.subplots(1, 3)
        
        ax[0].imshow(image, cmap='gray')
        ax[0].set_title("Original Image")
        ax[0].axis('off')
        
        ax[1].plot(bin_centers, hist, lw=2)
        ax[1].set_title("Histogram")
        ax[1].set_xlabel("Intensity Value")
        ax[1].set_ylabel("Pixel Count")
        ax[1].axvline(ret, color='r', linestyle='--', lw=2)  # mark the threshold
        
        ax[2].imshow(segmented, cmap='gray')
        ax[2].set_title("Segmented Image")
        ax[2].axis('off')
        
        plt.show()

    def region_based_segmentation(self,   img_path: str):
        image = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        _, binary_image = cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        num_labels, labels_im = cv2.connectedComponents(binary_image)

        fig, ax = plt.subplots(1, 2)
        ax[0].imshow(image, cmap='gray')
        ax[0].set_title("Original image")
        ax[1].imshow(labels_im, cmap='nipy_spectral')
        ax[1].set_title("Region-based segmentation")

        plt.show()
 
    
class NoiseRemoval:
    def remove_noise(self, img_path: str):
        image = cv2.imread(img_path)
        # h : parameter deciding filter strength. Higher h value removes noise better, but removes details of image also. (10 is ok)
        # hForColorComponents : same as h, but for color images only. (normally same as h)
        # templateWindowSize : should be odd. (recommended 7)
        # searchWindowSize : should be odd. (recommended 21)

        denoised = cv2.fastNlMeansDenoisingColored(image, None, 10, 10, 7, 21)
        
        _, ax = plt.subplots(1, 2)
        ax[0].imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
        ax[0].set_title("Original image")
        ax[1].imshow(cv2.cvtColor(denoised, cv2.COLOR_BGR2RGB))
        ax[1].set_title("Denoised image")
        plt.show() 

# io = ImageUtils() 

# Show image
# io.show_image('flower.jpg')

# Image from random
# io.image_from_random()

# Rotate
# io.rotate_image('flower.jpg', 45, resize=True, fill_color=ImageColor.getcolor('red', 'RGB'))

# Resize
# io.resize_image('flower.jpg', (200, 200))

# Quantize
# io.quantize_image('flower.jpg', quantised_colors=2)

# Histogram
# io.generate_histogram('flower.jpg')

# Equalize historagm
# io.equalize_histogram('flower.jpg')


# Padding
# padding = Padding()

# zero padding
# padding.zero_padding('flower.jpg', 50)

# constant padding
# padding.constant_padding('flower.jpg', 50)

# nearest neighbour padding
# padding.nearest_neighbour_padding('flower.jpg', 50)

# reflect padding
# padding.reflect_padding('flower.jpg', 50)

# Filters
# filters = Filters()

# mean filter
# filters.mean_filter('flower.jpg', 5)

# filters.min_filter('flower.jpg', 5)

# filters.median_filter('flower.jpg', 5)

# filters.max_filter('flower.jpg', 5)


# Edge detection

# edge = EdgeDetection()
# edge.sobel_detection('flower.jpg', 9)
# edge.canny_detection('flower.jpg')
# edge.laplacian('flower.jpg')
# edge.laplacian_of_gaussian('flower.jpg', 3) 

# Image enhancement
# enhancer = ImageEnhancement()
# enhancer.power_law_transformation('flower.jpg', 0.7)
# enhancer.log_transformation('flower.jpg')

# Morphological operations
# morph = MorphologicalOperations()

# morph.hit_or_miss('flower.jpg')
# morph.thicken('flower.jpg')
# morph.thin('flower.jpg', (3, 3))
# morph.skeletonize_image('flower.jpg')

# convolutions = Convolutions()

# convolutions.ideal_lowpass_filter('flower.jpg', 30)
# convolutions.gaussian_lowpass_filter('flower.jpg', 5)
# convolutions.gaussian_highpass_filter('flower.jpg', 5)


# segment = Segmentation()

# segment.histogram_segmentation('flower.jpg')
# segment.region_based_segmentation('flower.jpg')

removal = NoiseRemoval()
removal.remove_noise('girl.jpg')
