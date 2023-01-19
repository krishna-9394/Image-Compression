from PIL import Image


def RLE_compress_image(image_path):
    # Open the image
    with Image.open(image_path) as image:
        # Get image data
        image_data = image.getdata()
        # Initialize variables for compression
        current_pixel = None
        current_count = 0
        compressed_data = []
        # Iterate through image data
        for pixel in image_data:
            # If this is the first pixel or the same as the previous pixel
            if current_pixel == pixel:
                current_count += 1
            else:
                # If this is a new pixel, append the previous count and pixel to the compressed data
                if current_pixel is not None:
                    compressed_data.append((current_count, current_pixel))
                current_pixel = pixel
                current_count = 1
        # Append the last count and pixel to the compressed data
        compressed_data.append((current_count, current_pixel))
        return compressed_data


def Lossless_compress_image_and_save(image_path, output_path):
    # Compress the image
    compressed_data = RLE_compress_image(image_path)
    # Open the image
    with Image.open(image_path) as image:
        # Create a new image with the same mode and size as the original
        output_image = Image.new(image.mode, image.size)
        # Get the output image pixel data
        output_data = output_image.load()
        # Initialize variables for decompression
        x = 0
        y = 0
        # Iterate through the compressed data
        for count, pixel in compressed_data:
            # Draw the pixel count times in the output image
            for i in range(count):
                output_data[x, y] = pixel
                x += 1
                if x == image.width:
                    x = 0
                    y += 1
        # Save the output image
        output_image.save(output_path)



