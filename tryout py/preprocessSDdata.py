from PIL import Image, ExifTags
import os

# Define the input and output directories
input_dir = 'C://Users//karthikeya//Downloads//karthispace'
output_dir = 'C://Users//karthikeya//Desktop//karthispace'

# Create output directory if it doesn't exist
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Function to correct image orientation based on EXIF data
def correct_orientation(img):
    try:
        for orientation in ExifTags.TAGS.keys():
            if ExifTags.TAGS[orientation] == 'Orientation':
                break

        exif = img._getexif()

        if exif is not None:
            orientation = exif.get(orientation)

            if orientation == 3:
                img = img.rotate(180, expand=True)
            elif orientation == 6:
                img = img.rotate(270, expand=True)
            elif orientation == 8:
                img = img.rotate(90, expand=True)
    except (AttributeError, KeyError, IndexError):
        pass

    return img

# Function to resize and compress images
def resize_and_compress_image(image_path, output_path, size=(512, 512), quality=85):
    with Image.open(image_path) as img:
        # Correct orientation
        img = correct_orientation(img)
        # Resize the image
        img = img.resize(size, Image.LANCZOS)
        # Save the image with compression
        img.save(output_path, format='JPEG', quality=quality)

# Loop through each image in the input directory
for filename in os.listdir(input_dir):
    if filename.endswith(('.jpg', '.jpeg', '.png')):
        input_path = os.path.join(input_dir, filename)
        output_path = os.path.join(output_dir, filename)
        resize_and_compress_image(input_path, output_path)

print("Images have been resized and compressed.")
