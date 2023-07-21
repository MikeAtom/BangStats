# Module description:
# This module is used to read all the text from the image and return it as a list of strings.
# output: [([bbox], text), ([bbox], text), ... , ([bbox], text)]


import cv2
import easyocr
import shutil

debug = 0

tempFolder = "data/images/_temp.png"


def show_cropped_image(top_left, bottom_right):
    image = cv2.imread(tempFolder)
    cv2.imshow('crop', image[top_left[1]:bottom_right[1], top_left[0]:bottom_right[0]])
    cv2.waitKey(0)


# Brightness and contrast
def brightness_contrast(image, brightness, contrast):
    if brightness != 0:
        if brightness > 0:
            shadow = brightness
            highlight = 255
        else:
            shadow = 0
            highlight = 255 + brightness
        alpha_b = (highlight - shadow) / 255
        gamma_b = shadow

        buf = cv2.addWeighted(image, alpha_b, image, 0, gamma_b)
    else:
        buf = image.copy()

    if contrast != 0:
        f = 131 * (contrast + 127) / (127 * (131 - contrast))
        alpha_c = f
        gamma_c = 127 * (1 - f)

        buf = cv2.addWeighted(buf, alpha_c, buf, 0, gamma_c)

    return buf


# Gray scale image
def grayscale(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)


# OCR
def ocr(imagePath, onGPU):
    print("Reading text from image: " + imagePath)
    
    # Copy image to temp folder
    shutil.copyfile(imagePath, tempFolder)
    
    # Read image
    image = cv2.imread(tempFolder)

    # resize image to 720 height
    height, width = image.shape[:2]
    ratio = height / 720
    image = cv2.resize(image, (int(width / ratio), int(height / ratio)))

    # Crop image to 1280 width with anchor point at center
    height, width = image.shape[:2]
    anchor = int(width / 2)
    image = image[0:720, anchor - 640:anchor + 640]

    # Preprocess image
    image = grayscale(image)  # grayscale

    # Read text from image using easyocr
    reader = easyocr.Reader(['en'], gpu=onGPU)

    # Format output
    output = reader.readtext(image)

    if debug:

        for (coord, text, prob) in output:
            (topleft, topright, bottomright, bottomleft) = coord
            tx, ty = (int(topleft[0]), int(topleft[1]))
            bx, by = (int(bottomright[0]), int(bottomright[1]))
            cv2.rectangle(image, (tx, ty), (bx, by), (0, 0, 255), 2)

        cv2.imshow("Image", image)
        cv2.waitKey(0)

    output = [([b[0][0], b[0][1], b[0][2], b[0][3]], b[1]) for b in output]

    #print(output)

    return output


"""
    if False:
        print(output)

        for (coord, text, prob) in output:
            (topleft, topright, bottomright, bottomleft) = coord
            tx, ty = (int(topleft[0]), int(topleft[1]))
            bx, by = (int(bottomright[0]), int(bottomright[1]))
            cv2.rectangle(image, (tx, ty), (bx, by), (0, 0, 255), 2)

        cv2.imshow("Image", image)
        cv2.waitKey(0)
        
    
    # save image to temp folder
    cv2.imwrite(tempFolder, image)

"""
