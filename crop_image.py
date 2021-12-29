import cv2
import os


def upscaling(image, x=300, y=300):
    resized_image = cv2.resize(image, (x, y), interpolation=cv2.INTER_AREA)
    return resized_image


def show_image(name, image):
    cv2.imshow(name, image)
    cv2.waitKey(0)


img = cv2.imread(os.path.join(os.getcwd(), 'photos', 'original', 'payload.png'))

height, width, channels = img.shape
print(height, 'x', width)

cv2.imshow('image', img)
cv2.waitKey(100)

images = []

step = 100
height = 0
width = 0
for i in range(3):
    for j in range(3):
        images.append(img[width: width + step, height: height + step])
        width += step
    width = 0
    height += step

for i in range(9):
    cv2.imshow('img' + str(i), images[i])
    cv2.waitKey(100)
    cv2.imwrite(os.path.join(os.getcwd(), 'photos', 'cropped', f'img{i}.jpg'), images[i])

cv2.destroyAllWindows()
