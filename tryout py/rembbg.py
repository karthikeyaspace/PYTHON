import os
from rembg import remove
from PIL import Image

def remove_background(input_path, output_path):
    for filename in os.listdir(input_path):
        img = os.path.join(input_path, filename)

        if(img.endswith(('.png', '.jpg', '.jpeg'))):
            with Image.open(img) as i:
                i_rembg = remove(i.convert("RGB"))
                op = os.path.join(output_path,filename)
                i_rembg.save(op)
        
        



input_path = 'D:/KARTHIKEYA/PROJECTS/VS CODE/FULLSTACK/vjdataquesters-website/FRONTEND/public/teamImages'
output_path = 'D:/KARTHIKEYA/PROJECTS/VS CODE/FULLSTACK/vjdataquesters-website/FRONTEND/public/teamImagesBgRemoved'
remove_background(input_path, output_path)