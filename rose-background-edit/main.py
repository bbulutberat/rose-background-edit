import cv2 
import numpy as np

class GörüntüIsleme():

    def __init__(self, image):

        self.image = cv2.imread(image)
        self.hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
    
    def maske_olusturma(self, lower, upper):

        self.mask = cv2.inRange(self.hsv, lower, upper)
        return self.morfolojik_islem(self.mask)
    
    def morfolojik_islem(self, mask):

        kernel = np.ones((15,15), np.uint8)
        closing = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel, iterations=1)
        kernel = np.ones((3,3), np.uint8)
        self.mask = cv2.erode(closing, kernel, iterations=1)
        return self.maskeleme()
    
    def maskeleme(self):

        self.output = cv2.bitwise_and(self.hsv, self.hsv, mask=self.mask)
        return self.mask
    
    def renk_degistir(self):

        h, s, v = cv2.split(self.output)
        h[self.mask==255] = 140
        self.output = cv2.merge([h,s,v])
        self.output = cv2.cvtColor(self.output, cv2.COLOR_HSV2BGR)
        return self.output
    
    def islem_baslat(self, lower, upper):

        mask = self.maske_olusturma(lower,upper)
        output = self.renk_degistir()
        return mask, output

if __name__ == "__main__": 

    image = "image\input.jpg"
    islem = GörüntüIsleme(image)
    
    lower = np.array([111, 27, 0])
    upper = np.array([180, 255, 255])

    mask, output = islem.islem_baslat(lower, upper)

    cv2.imshow("mask", mask)
    cv2.imshow("output", output)

    cv2.imwrite("image\output.jpg", output)

    cv2.waitKey(0)
    cv2.destroyAllWindows()



