import cv2 as cv
import numpy as np
import numpy as np

def split_by_cont(uploaded_file):
    # Read the uploaded image using OpenCV
    image_data = uploaded_file.read()
    nparr = np.frombuffer(image_data, np.uint8)
    img = cv.imdecode(nparr, cv.IMREAD_COLOR)
    
    #process
    height,width,_ = img.shape
    scale=1/4
    if width*height>1000000:scale=1/4
    if width*height<1000000 and width*height>500000:scale=1/2
    if width*height<500000 and width*height>100000:scale=1
    if width*height<100000:scale=2
    width = int(width*scale)
    height = int(height*scale)
    img = cv.resize(img,(width,height))
    imgFilter = cv.bilateralFilter(img,9,45,45)
    img = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    edges=cv.Canny(imgFilter,100,200)

    #cut by contour
    image = cv.bitwise_not(edges)
    _, binary_image = cv.threshold(image, 128, 255, cv.THRESH_BINARY_INV)
    contours, _ = cv.findContours(binary_image, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    filled_image = np.zeros_like(binary_image)
    for contour in contours:
        cv.fillPoly(filled_image, [contour], color=(255, 255, 255))
    items = []
    for i, contour in enumerate(contours):
        x, y, w, h = cv.boundingRect(contour)
        item = filled_image[y-5:y + h+5, x-5:x + w+5]
        item=cv.bitwise_not(item)
        items.append(item)

    return items