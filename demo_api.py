# -*- coding: utf-8 -*-

import cv2
import time
import json                    
import requests
from PIL import Image
from io import BytesIO

#選擇攝影機
cap = cv2.VideoCapture(0)

#設定影像大小
wCam, hCam = 320, 240


cap.set(3, wCam)
cap.set(4, hCam)

pTime = 0

# Vision API
#url = 'http://34.80.31.212/tdri/api/vision/analyze?return_features=pose'  
url = 'http://localhost:5000/api/PredictPose'
i = 0
l = []
while True:
    
    success, image = cap.read()
    cTime = time.time()
    
    fps = 1 / (cTime - pTime)
    #print(fps)
    pTime = cTime
    if len(l)>10:
        l = []
        
    # 我的相機大約30FPS，所以設定大約每秒 10 張
    if i%1==0:    
##################################################################################
        try:
            print(pTime)
            frame_im = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            pil_im = Image.fromarray(frame_im)
            stream = BytesIO()
            pil_im.save(stream, format="JPEG")
            stream.seek(0)
            img_for_post = stream.read()
            
            start = time.time()
            files = {'image': img_for_post}
            r = requests.post(
                url,
                files=files
            )

            end = time.time()
            
            #平均回傳時間
            print("Response time:" + str(end-start))
            result = json.loads(r.text)
            #result = result["feature_list"][0]['pose_list'][0]['label']
            result = result['pose_list'][0]['label']
            l.append(result)
            print(l)
        except Exception:
            result = "none"
##################################################################################
    cv2.putText(image, str(result),(45, 375), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 1, cv2.LINE_AA)
    i = i+1
    cv2.imshow("Image", image)
    
#按Q建結束
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
