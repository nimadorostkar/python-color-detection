import numpy as np 
import argparse
import cv2 

def main():

    RGB_CODES = {}
    with open('colors.txt') as f:
        colors = f.readlines()
        for color in colors:
            name, r, g, b = color.split()
            RGB_CODES[name] = list(map(int, [r, g, b][::-1]))

    print("Color Detector python.")
    print('-'*100)
    print("The available colors: ", end="")
    print(*RGB_CODES.keys(), sep=", ")
    print('-'*100)
    print("1) To detect the color in an image.")
    print("2) To add a new color.")
    print("3) To delete a color.")
    choice = int(input("Your choice: "))
    print('-'*100)

    if choice == 1:
        file_name = input("Enter the file's name with extension: ")
        image = cv2.imread(file_name)
        color_name = input("Enter the color's name: ")
        if color_name not in RGB_CODES.keys():
            raise Exception("Wrong Choice.")
        else:
            color = np.uint8([[RGB_CODES[color_name]]])
            hsv_color= cv2.cvtColor(color, cv2.COLOR_BGR2HSV)
            h = hsv_color[0][0][0]
            print(hsv_color)

            lower_bound = np.uint8([h-10, 100, 100])
            upper_bound = np.uint8([h+10, 255, 255])

            if color_name == "red":
                lower_bound = np.uint8([0, 50, 50])
                upper_bound = np.uint8([10, 255, 255]) # can't figure out why red's code doesn't work when I use h-10, 100, 100 and h+10, 255, 255 as the limits.

            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            mask = cv2.inRange(hsv, lower_bound, upper_bound)
            output = cv2.bitwise_and(image, image, mask=mask)

            cv2.namedWindow('image', cv2.WINDOW_NORMAL)
            cv2.resizeWindow('image', 800, 800)
            cv2.imshow('image', np.hstack([image, output]))
            cv2.waitKey(0)
    elif choice == 2:
        color_name = input("Enter the color's name: ")
        color_code = input("Enter the color's values of r, g, b seprated by a space: ")
        with open("colors.txt", 'a') as f:
            f.write('\n'+color_name+" "+color_code)
    elif choice == 3:
        color_name = input("Enter the color's name: ")
        with open("colors.txt") as f:
            data = f.readlines()
            data = [x for x in data if x.split()[0] != color_name]
        with open("colors.txt", 'w') as f:
            f.writelines(data)
    else:
        raise Exception("Wrong Choice.")

if __name__ == "__main__":
    main()
