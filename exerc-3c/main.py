import numpy as np
import argparse, cv2, glob, sys
import datetime

ap = argparse.ArgumentParser()
ap.add_argument("-t", "--target", required = True, help = "Is the file used as reference for the comparison")
ap.add_argument("-d", "--dataset", required = True, help = "Path to the directory of images")
args = vars(ap.parse_args())

histograms = {}
images = {}

OPENCV_METHODS = (
    ("Correlation", cv2.HISTCMP_CORREL),
    ("Chi-Squared", cv2.HISTCMP_CHISQR),
    ("Intersection", cv2.HISTCMP_INTERSECT),
    ("Bhattacharyya", cv2.HISTCMP_BHATTACHARYYA)
)

def calculateHist(image):
    return cv2.calcHist([image], [0, 1, 2], None, [256,256,256],[0, 256, 0, 256, 0, 256])

# load dataset
for imagePath in glob.glob(args["dataset"] + "/*"):
    filename = imagePath[imagePath.rfind("/") + 1:]
    print "Loading: {}".format(imagePath)
    image = cv2.imread(imagePath)
    images[filename] = cv2.cvtColor(image, cv2.COLOR_BGR2RGB) #convert BGR to RGB for matplotlib
    histograms[filename] = calculateHist(image)

# load target image
print "Loading target image: {}".format(args["target"])
target = cv2.imread(args["target"])
target = cv2.cvtColor(target, cv2.COLOR_BGR2RGB)
target_hist = calculateHist(target)

summary = []

for (methodName, method) in OPENCV_METHODS:
    results = []
    reverse = False

    if methodName in ("Correlation", "Intersection"):
        reverse = True

    for (name, hist) in histograms.items():
        r = cv2.compareHist(target_hist, hist, method)
        results.append((name,r))

    results = sorted([(v, k) for (k, v) in results], reverse = reverse)
    summary.append((methodName,results))

    print "\nFor method {} the results are:".format(methodName)
    print "\n -> Order number zero is the best match.\n"
    print "Order | Score | Image"

    for (i, (v, k)) in enumerate(results):
        print "{} | {} | {} ".format(i,v,k)

# print summary
