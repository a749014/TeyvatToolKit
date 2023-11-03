import cv2 as cv
from matplotlib import pyplot as plt
image=cv.imread(r'D:\TeyvatToolKit\opencv_learning\images\OIP-C.jpg',-1)
video=cv.VideoCapture(r'D:\TeyvatToolKit\opencv_learning\images\OIP-C.jpg)
image=cv.cvtColor(image,cv.COLOR_BGR2RGB)
print(image)
plt.imshow(image)
# plt.gray()
plt.show()