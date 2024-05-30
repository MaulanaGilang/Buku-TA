from PIL import Image
import os
from tqdm import tqdm

# Load the images
line_path = os.path.join('noairgap', 'line.png')
wave_path = os.path.join('noairgap', 'wave.png')

line_img = Image.open(line_path)
wave_img = Image.open(wave_path)

# Create a new image with the same size as the line image but with alpha to composite images over it
result_img = Image.new('RGBA', (1860, 1160), (255, 255, 255, 0))

# Paste the line image at (0, 0)
result_img.paste(line_img, (0, 0), line_img)

# Function to apply transformations and save the results
def transform_and_save(wave_img, result_img, shift_x, shift_y, crop_size, file_name):
    temp_img = result_img.copy()
    # Paste the wave image at (0, 0) with the specified horizontal and vertical shifts
    temp_img.paste(wave_img, (shift_x, shift_y), wave_img)
    temp_img.paste(line_img, (0, 0), line_img)
    # Crop the image
    cropped_img = temp_img.crop((0, 0, crop_size[0], crop_size[1]))
    # Save the image
    cropped_img.save(file_name)

crop_size = (1860, 1160)

wave_width, wave_height = wave_img.size
horizontal_step = 5
vertical_step = 20
vertical_limit = 100

print("It will generate", (wave_width - 1860) // horizontal_step * (vertical_limit // vertical_step + 1), "images")

counter = 0
for horizontal_shift in tqdm(range(-wave_width + 1860, 0, horizontal_step)):
  for vertical_shift in range(0, vertical_limit + 1, vertical_step):
    file_name = f'noairgap/fix/data_{counter}.png'
    transform_and_save(wave_img, result_img, horizontal_shift, vertical_shift, crop_size, file_name)
    counter += 1