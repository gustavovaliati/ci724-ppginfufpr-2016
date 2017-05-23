#!/usr/bin/python

import numpy as np
import cv2, sys, scipy

import matplotlib
matplotlib.use('Agg') # Force matplotlib to not use any Xwindows backend.
from matplotlib import pyplot as plt


img = cv2.imread('blob.png')
imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
thresh = abs(imgray - 255)
img2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
# img2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# img2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
# img2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_L1)
# img2, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_TC89_KCOS)

cv2.drawContours(img, contours, -1, (0,255,0), 1)

hists_diff_chains = {}
hists_chains = {}

map = { 0 : [0,1,2,3], 1: [1,2,3,0], 2: [2,3,0,1], 3: [3,0,1,2] }
def calc_diff(a,b):
    way = map[a]
    for diff,val in enumerate(way):
        if val == b:
            return diff;

for j, obj in enumerate(contours):
    last_y = False
    last_x = False
    cur_chain = []
    diff_chain = []

    font = cv2.FONT_HERSHEY_SIMPLEX
    c_y,c_x = obj[0][0]
    cv2.putText(img,str(j),(c_y,c_x), font, 0.25,(0,0,0), 1,cv2.LINE_AA)

    for cont in obj:
        y,x = cont[0]
        if not last_x and not last_y:
            last_y = y;
            last_x = x;
            # print "primeiro"
            continue;

        '''
        MAP
        0 = RIGHT
        1 = UP
        2 = LEFT
        3 = DOWN
        '''
        if y == last_y and x > last_x: # RIGHT
            cur_chain.append(0)
        elif y < last_y and x == last_x: # UP
            cur_chain.append(1)
        elif y == last_y and x < last_x: # LEFT
            cur_chain.append(2)
        else: # DOWN
            cur_chain.append(3)

        last_y = y;
        last_x = x;

    # print cur_chain

    first_val = True
    for i,val in enumerate(cur_chain):
        if first_val:
            last_val = cur_chain[i]
            first_val = False
            continue

        cur_val = cur_chain[i]
        diff_chain.append(calc_diff(last_val, cur_val))
        last_val = cur_val

    # print diff_chain
    hist_chain = []
    hist_chain.append(cur_chain.count(0));
    hist_chain.append(cur_chain.count(1));
    hist_chain.append(cur_chain.count(2));
    hist_chain.append(cur_chain.count(3));
    hists_chains[j] = hist_chain

    hist_diff = []
    hist_diff.append(diff_chain.count(0));
    hist_diff.append(diff_chain.count(1));
    hist_diff.append(diff_chain.count(2));
    hist_diff.append(diff_chain.count(3));
    hists_diff_chains[j] = hist_diff

cv2.imwrite("contornado.png", img)

for j in hists_chains:
    # print hist_diff
    plt.plot(hists_chains[j], label=str(j))
    plt.xlim(0,3)
    plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
    plt.savefig("hist{}.png".format(j))

plt.clf()

for j in hists_diff_chains:
    # print hist_diff
    plt.plot(hists_diff_chains[j], label=str(j))
    plt.xlim(0,3)
    plt.legend(bbox_to_anchor=(1, 1), loc=2, borderaxespad=0.)
    plt.savefig("hist-diff{}.png".format(j))

def calcEuclideanDistance(a, b):
    a = np.array(a)
    b = np.array(b)
    d = np.linalg.norm(a-b)
    return d

summary = {}

def build_results(chains_array, type):
    print "\n --- Calculations for chaincodes: {} --- \n".format(type)
    for hist_a_index in chains_array:
        print "Calculating object {} .".format(hist_a_index)
        distances = []
        map = {}
        for hist_b_index in chains_array:
            if hist_a_index == hist_b_index:
                continue
            distance = calcEuclideanDistance(chains_array[hist_a_index], chains_array[hist_b_index])
            distances.append(distance)
            map[str(distance)] = hist_b_index
            print "Distance from {} to {} = {}".format(hist_a_index, hist_b_index, distance)
        result = "{}: The most similar object to {} is {}.".format(type,hist_a_index, map[str(min(distances))])
        print result
        if hist_a_index not in summary:
            summary[hist_a_index] = []

        summary[hist_a_index].append(result)

build_results(hists_chains, "without_differences")
build_results(hists_diff_chains, "with_differences")

print "\n --- Summary --- \n"

for item in summary:
    print "For object {}:".format(item)
    for i in summary[item]:
        print i
