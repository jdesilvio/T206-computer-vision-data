# Extract SIFT features from images

import numpy as np
import cv2

class CardDescriptor:
    def __init__(self, kpMethod="SIFT", descMethod="SIFT"):
        self.kpMethod = kpMethod
        self.descMethod = descMethod

    # Extract key points and descriptors for an image
    def describe(self, image):
        sift = cv2.xfeatures2d.SIFT_create()
	#detector = cv2.FeatureDetector_create(self.kpMethod)
        #kps = detector.detect(image)

        #extractor = cv2.DescriptorExtractor_create(self.descMethod)
        #(kps, descs) = extractor.compute(image, kps)
        
	(kps, descs) = sift.detectAndCompute(image, None)

	kps = np.float32([kp.pt for kp in kps])
        print str(image)
        print (kps, descs)
	return (kps, descs)
