import numpy as np
import argparse, cv2

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--input", required = True, help = "Origin colored image.")
ap.add_argument("-o", "--output", required = True, help = "Path for the output gray image")
args = vars(ap.parse_args())

gray = cv2.imread(args["input"], 0)
cv2.imwrite(args["output"], gray)

print "Done."
