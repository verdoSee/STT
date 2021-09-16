import os
import pygame
import pyautogui
import pyperclip
import pytesseract
from PIL import Image
import win32gui, win32con

#hiding console after opening the program
hide = win32gui.GetForegroundWindow()
#comment this out if you run in IDE
win32gui.ShowWindow(hide, win32con.SW_HIDE)

pygame.init()

#taking screenshot of desktop to use as background (faking transparency as windows 10 screenshot tool does)
pyautogui.screenshot("bg.png",region=(0, 0, 1920, 1080))

#opening window
screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)

#making focus surface
focus = pygame.Surface((1920, 1080), pygame.SRCALPHA) 

#background image
bg = pygame.image.load("bg.png") 
os.remove("bg.png")

# checks
done = False
check = 0
check1 = 0

#colors used
white = (255, 255, 255)
semiTransparent = (0 ,0 ,0 ,128)
transparent = (0, 0, 0, 0)

#text 
font = pygame.font.Font('freesansbold.ttf', 25) 
texto=font.render('Press "q" to define one corner and again to define the rectangle', True, white)

#grey scaling the image
def grayify(image):
    imgs = Image.open(image).convert('L')
    return imgs

while not done:
    key = pygame.key.get_pressed()
    pygame.time.delay(50)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    # getting cursor positions to later use to draw the rectangle
    if check1 == 0:
        #cheking for "q" press
        if key[pygame.K_q]:
            if check == 0:
                check = 1
                t = win32gui.GetCursorPos()
            else:
                done = True
                break
            #this prevents double checks in case the button is holded too much
            check1 = 10

        else:
            b = win32gui.GetCursorPos()
    else:
        check1 -= 1

    #area outside drag-select will be "out of focus"
    focus.fill(semiTransparent) 

    # draw rectangle
    if check == 1:
        pygame.draw.rect(focus,white,(min(t[0], b[0]) - 1,min(t[1], b[1]) - 1,abs(b[0] - t[0]) + 2,abs(b[1] - t[1]) + 2,),1)
        focus.fill(transparent,(min(t[0], b[0]), min(t[1], b[1]), abs(b[0] - t[0]), abs(b[1] - t[1])))
    #blit the image in the screen
    screen.blit(bg, (0, 0))
     #blit the focus in the screen
    screen.blit(focus, (0, 0))
    #blit the text in the screen
    screen.blit(texto, (0,0)) 

    pygame.display.update()

#screenshot for tesseract
pyautogui.screenshot(
    "img2text.png",region=(min(t[0], b[0]), min(t[1], b[1]), abs(b[0] - t[0]), abs(b[1] - t[1]))
)

pygame.display.quit()

#locating tesseract
pytesseract.pytesseract.tesseract_cmd = (
    r"C:\\Program Files\\Tesseract-OCR\\tesseract.exe"
)

#grey scaling the image
grayify("img2text.png").save("greyscaled.png")
os.remove("img2text.png")

#from image to string
text = pytesseract.image_to_string("greyscaled.png")
os.remove("greyscaled.png")

#removing  character that tesseract adds as a default in the end
text = text.rstrip(text[-1]) 

#copying the text in the clipboard
pyperclip.copy(text)

