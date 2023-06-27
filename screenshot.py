from PIL import Image, ImageTk
import cv2
import time
import os

def crop_boundary(cv_image):
    (shot_height, shot_width, _) = cv_image.shape

    check_interval = 100
    minx, miny, maxx, maxy = shot_width, shot_height, 0, 0
    for i in range(0, shot_height):
        sample = [ cv_image[i][j] for j in range(0, shot_width, check_interval) ]
        if any([ pixel[0] != 0 or pixel[1] != 0 or pixel[2] != 0 for pixel in sample ]):
            miny = i
            break
    for i in range(0, shot_height):
        col_index = shot_height - i - 1
        sample = [ cv_image[col_index][j] for j in range(0, shot_width, check_interval) ]
        if any([ pixel[0] != 0 or pixel[1] != 0 or pixel[2] != 0 for pixel in sample ]):
            maxy = col_index
            break
    for i in range(0, shot_width):
        sample = [ cv_image[j][i] for j in range(0, shot_height, check_interval) ]
        if any([ pixel[0] != 0 or pixel[1] != 0 or pixel[2] != 0 for pixel in sample ]):
            minx = i
            break
    for i in range(0, shot_width):
        row_index = shot_width - i - 1
        sample = [ cv_image[j][row_index] for j in range(0, shot_height, check_interval) ]
        if any([ pixel[0] != 0 or pixel[1] != 0 or pixel[2] != 0 for pixel in sample ]):
            maxx = row_index
            break
    return cv_image[miny:maxy, minx:maxx]

def take_screenshot(window_id, frame=None, mask=None):
    if window_id is None:
        return None, None

    prev = time.time()
    img_file_name = 'scrshot/screenshot.png'
    # -x mutes sound and -l specifies windowId
    os.system('screencapture -x -l %s %s' % (window_id, img_file_name))
    print(time.time() - prev)

    cv_image = cv2.imread(img_file_name)
    cv_image = cv2.cvtColor(cv_image, cv2.COLOR_BGRA2RGBA)
    org_height, org_width, _ = cv_image.shape
    if frame is not None:
        frame_width, frame_height = frame
        if org_width > frame_width or  org_height > frame_height:
            ratio = min(frame_width / org_width, frame_height / org_height)
            cv_image = cv2.resize(cv_image, (int(org_width * ratio), int(org_height * ratio)), interpolation = cv2.INTER_AREA)

    cv_image = crop_boundary(cv_image)
    if mask is not None:
        ( left, right, top, bottom ) = mask
        cv_image = cv_image[top:bottom, left:right]

    current_image = Image.fromarray(cv_image)

    img = ImageTk.PhotoImage(current_image)
    return ( img, (org_width, org_height) )