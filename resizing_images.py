from PIL import Image


def resize_image (fpath, output_filename="", width = 1400, height = 1400, quality = 30):
    try :
        #open the image
        with Image.open(fpath) as im:
            im_resized = im.resize((width, height))
            im_resized.save(output_filename, quality = quality)
    except Exception as e:
        print(f"error resizing image :  {e}")
        return None