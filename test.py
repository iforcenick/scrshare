from PIL import ImageGrab
import time

prev = time.time()
screenshot = ImageGrab.grab()
print(time.time() - prev)
screenshot.show()