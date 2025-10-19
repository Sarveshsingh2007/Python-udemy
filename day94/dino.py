import pyautogui
from PIL import ImageGrab
import time
import webbrowser

# Step 1: Open the game automatically
webbrowser.open("https://elgoog.im/t-rex/")
time.sleep(5)  # wait for the browser to open

print("Get ready! The bot will start in 3 seconds...")
time.sleep(3)
print("Bot is running... Press Ctrl + C to stop.")

def is_collide(data, width, height):
    """
    Detect obstacles in the screenshot region.
    We'll check a small area for dark pixels (obstacles).
    """
    for x in range(int(width * 0.6), width):   # check near right edge
        for y in range(int(height * 0.4), int(height * 0.9)):  # check ground level
            if data[x, y] < 100:  # dark obstacle
                return True
    return False

def hit(key):
    pyautogui.keyDown(key)
    time.sleep(0.05)
    pyautogui.keyUp(key)

while True:
    # Step 2: Capture region in front of the dinosaur
    # You might need to adjust bbox for your screen resolution.
    image = ImageGrab.grab(bbox=(300, 380, 500, 460))
    gray = image.convert('L')
    data = gray.load()
    width, height = gray.size
                    
    # Step 3: Check for obstacle
    if is_collide(data, width, height):
        hit("space")
        print("Jump!")

    # Optional: slow down loop slightly if CPU usage is high
    # time.sleep(0.01)
