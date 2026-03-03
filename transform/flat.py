import os
import shutil

# base folder where your folders are present
base_dir = "/Users/ajoe01/Documents/tim/sql-practice/linkedin_posts"
output_dir = os.path.join(base_dir, "flattened")

os.makedirs(output_dir, exist_ok=True)

counter = 1

for folder in sorted(os.listdir(base_dir)):
    folder_path = os.path.join(base_dir, folder)

    if os.path.isdir(folder_path):
        txt_path = os.path.join(folder_path, "content.txt")
        img_path = os.path.join(folder_path, "image_1.jpg")

        if os.path.exists(txt_path):
            shutil.copy(txt_path, os.path.join(output_dir, f"day_{counter}.txt"))

        if os.path.exists(img_path):
            shutil.copy(img_path, os.path.join(output_dir, f"day_{counter}.jpg"))

        counter += 1

print(f"✅ Done. Files are saved in: {output_dir}")
