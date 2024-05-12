import os
import random
from shutil import copyfile

# Set the paths for your dataset
image_folder = "M:\sem8\FYP2\POLAR\hvnsh7rwz7-1\JPEGImages\JPEGImages"
label_folder = "M:\sem8\FYP2\POLAR\hvnsh7rwz7-1\JPEGImages\JPEGImages"
output_folder = "M:\sem8\FYP2\POLAR\hvnsh7rwz7-1\JPEGImages\POLARYOLO"

# Set the percentage split for train, test, and val
train_percent = 0.8
test_percent = 0.1
val_percent = 0.1

# Ensure the output folders exist
os.makedirs(os.path.join(output_folder, 'train'), exist_ok=True)
os.makedirs(os.path.join(output_folder, 'test'), exist_ok=True)
os.makedirs(os.path.join(output_folder, 'val'), exist_ok=True)

# Get the list of image files
image_files = [f for f in os.listdir(image_folder) if f.endswith('.jpg')]

# Randomly shuffle the list
random.shuffle(image_files)

# Calculate the number of images for each split
num_images = len(image_files)
num_train = int(train_percent * num_images)
num_test = int(test_percent * num_images)
num_val = num_images - num_train - num_test

# Split the dataset
train_images = image_files[:num_train]
test_images = image_files[num_train:num_train + num_test]
val_images = image_files[num_train + num_test:]

# Function to copy files to the respective folders
def copy_files(images, folder):
    for image in images:
        image_path = os.path.join(image_folder, image)
        label_path = os.path.join(label_folder, image.replace('.jpg', '.txt'))
        destination_path = os.path.join(output_folder, folder, image)
        destination_label_path = os.path.join(output_folder, folder, image.replace('.jpg', '.txt'))

        copyfile(image_path, destination_path)
        copyfile(label_path, destination_label_path)

# Copy files to the respective folders
copy_files(train_images, 'train')
copy_files(test_images, 'test')
copy_files(val_images, 'val')

print("Dataset split successfully.")
