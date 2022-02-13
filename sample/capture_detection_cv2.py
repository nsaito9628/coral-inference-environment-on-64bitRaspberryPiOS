#------------------------------------------------------------
#   coding:utf-8
#------------------------------------------------------------
#   Updata History
#   November  20  09:00, 2019 (Wed)
#------------------------------------------------------------
#
#   Raspberry Pi + Coral USB ACCELERATOR
#   Coral USBを用いたリアルタイム物体検出・顔検出
#
#   本プログラムではcv2.VideoCapture()を使用
#------------------------------------------------------------

import argparse
import time
import sys

import cv2 
import numpy as np
#import picamera
from edgetpu.detection.engine import DetectionEngine
from edgetpu.utils import dataset_utils
from PIL import Image, ImageDraw, ImageFont

import board
import neopixel
import datetime

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18
 
# The number of NeoPixels
num_pixels = 144
 
# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB
 
#pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.5, auto_write=False, pixel_order=ORDER)
pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.5, auto_write=True,
                           pixel_order=ORDER)


"""
    矩形の描画および表示
"""
def draw_image(th, image, results, labels):
    set_font = "/usr/share/fonts/truetype/piboto/Piboto-Regular.ttf"
    result_size = len(results)

    x_g = 0
    y_g = 0

    for idx, obj in enumerate(results):
        #  Prepare image for drawing
        draw = ImageDraw.Draw(image)

        #  Prepare boundary box
        box = obj.bounding_box.flatten().tolist()

        #  Annotate image with label and confidence score
        #if labels:
        if labels[obj.label_id] == "person" and obj.score > th:
            display_str = labels[obj.label_id] + ": " + str(round(obj.score*100, 2)) + "%"
            #draw.rectangle(box, outline=(0, 0, 255))
            x_g = int(box[2]-(box[2]-box[0])/2)
            y_g = int(box[3]-(box[3]-box[1])/2)
            draw.ellipse([(x_g - 30, y_g - 30), (x_g + 30, y_g + 30)], fill=(0, 0, 255), outline=(0, 0, 255))
            #print(box[0], box[1], box[2], box[3])
            #print(int(box[2]-(box[2]-box[0])/2), int(box[3]-(box[3]-box[1])/2))
            #draw.text((box[0], box[1]), display_str, font=ImageFont.truetype(set_font, 20))

    displayImage = np.asarray(image)
    cv2.imshow("Coral Live Object Detection", displayImage)

    return x_g #, y_g


"""
    Argumentsの設定
"""
def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
      '--model',
      help='Path of the detection model, it must be a SSD model with postprocessing operator.',
      required=True)
    parser.add_argument(
        "--label", help="Path of the labels file.")
    parser.add_argument(
        "--maxobjects", type=int, default=3, help="Maximum objects")
    parser.add_argument(
        "--threshold", type=float, default=0.05, help="Minimum threshold")
    parser.add_argument(
        "--picamera", action="store_true",
        help="Use PiCamera for image capture")
    parser.add_argument(
        '--keep_aspect_ratio',
        dest='keep_aspect_ratio',
        action='store_true',
        help=(
            'keep the image aspect ratio when down-sampling the image by adding '
            'black pixel padding (zeros) on bottom or right. '
            'By default the image is resized and reshaped without cropping. This '
            'option should be the same as what is applied on input images during '
            'model training. Otherwise the accuracy may be affected and the '
            'bounding box of detection result may be stretched.'))
    parser.set_defaults(keep_aspect_ratio=False)
    args = parser.parse_args()
    return args


"""
    メイン処理
"""
def main():
    #  Set up args
    args = parse_args()

    #  Initialize engine
    engine = DetectionEngine(args.model)
    labels = dataset_utils.read_label_file(args.label) if args.label else None

    #  Initialize video stream
    print("--------------------------------")
#    if not args.picamera:
    #  Set usb camera
    print("Use : usb camera")
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)#640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)#480)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M','J','P','G'))
    cap.set(cv2.CAP_PROP_FPS, 30)
    # cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc("H", "2", "6", "4"))
    # cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc("M", "J", "P", "G"))

    #  Camera error handling
    if cap.isOpened() == False:
        print("Cannot open")
        sys.exit(1)

#    else:
#        # Set picamera
#        print("Use : picamera")
#        cap = picamera.PiCamera()
#        cap.resolution = (1280, 720)#(640, 480)
#        cap.framerate = 30
    print("--------------------------------")

    pos_now = 0
    pos_bof = 0

    try:
        while True:
            #  Read frame from video
            _, img = cap.read()
            image = Image.fromarray(img)

            #  Perform inference
            results = engine.detect_with_image(
                image,
                threshold=args.threshold,
                keep_aspect_ratio=args.keep_aspect_ratio,
                relative_coord=False,
                top_k=args.maxobjects)

            #  draw image
            x_g = draw_image(args.threshold, image, results, labels)
            print("FPS: {}".format(cap.get(cv2.CAP_PROP_FPS)))

            try:
                pos_now = int (x_g * (num_pixels / 1280))
            except ZeroDivisionError:
                pass

            print(x_g, pos_now)

            #if pos_now == 0 :
            #    pass
            if pos_now > 0 and pos_now < num_pixels:
                pixels[pos_now] = (255, 0, 0)
                
            pixels[pos_bof] = (0, 0, 0)            
            pos_bof = pos_now

            #  closing confition
            if cv2.waitKey(5) & 0xFF == ord("q"):
                break

    except KeyboardInterrupt:
        print("Exit loop by Ctrl-c")
    
    print("FPS: {}".format(cap.get(cv2.CAP_PROP_FPS)))
    cap.release()
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()
