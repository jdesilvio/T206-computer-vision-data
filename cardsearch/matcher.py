# Match features

import numpy as np
import cv2
import h5py
import os

class CardMatcher:
    def __init__(self, descriptor):
        self.descriptor = descriptor

    # Compare the query image to each image in database and generate a score
    def search(self, queryKps, queryDescs):
        results = {}

        INDEX = os.path.join(os.path.dirname(__file__), '../testData/data.h5')

        # Read data from HDF5
        h5db = []
        with h5py.File(INDEX,'r') as hf2:
            for i in hf2['kps/']:
                k = hf2['kps/' + i][:]
                d = hf2['descs/' + i][:]
                h5db.append({"file": i, "desc": (k, d)})
	
        # Generate score
        for i in h5db:
            (kps, descs) = i["desc"]
            score = self.match(queryKps, queryDescs, kps, descs)
            results[i["file"]] = score
	print len(h5db)

        # Sort results
        if len(results) > 0:
            results = sorted([(v, k) for (k, v) in results.items() if v > 0], \
            reverse=True)

        return results

    # Algorithm to return keypoint and descriptor matches of 2 images
    def match(self, kpsA, featuresA, kpsB, featuresB, ratio=0.7, minMatches=50):
        matcher = cv2.DescriptorMatcher_create("BruteForce")
        rawMatches = matcher.knnMatch(featuresB, featuresA, 2)
        matches = []

        for m in rawMatches:
            if len(m) == 2 and m[0].distance < m[1].distance * ratio:
                matches.append((m[0].trainIdx, m[0].queryIdx))

        count = 0
        if len(matches) > minMatches:
            count += 1
            ptsA = np.float32([kpsA[i] for (i, _) in matches])
            ptsB = np.float32([kpsB[j] for (_, j) in matches])

            (_, status) = cv2.findHomography(ptsA, ptsB, cv2.RANSAC, 4.0)

            return float(status.sum()) / status.size

        return -1.0
