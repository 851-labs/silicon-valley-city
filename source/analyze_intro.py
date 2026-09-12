"""Measure the intro camera from static feature correspondences with the master still.

Requires the optional research environment and local production references.
Only numerical observations are written to source/; diagnostic images stay ignored.
"""
from pathlib import Path
import json,math
import cv2
import numpy as np
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'matching/intro_reference';OUT.mkdir(parents=True,exist_ok=True)
master=cv2.imread(str(ROOT/'references/original_wide.webp'))
cap=cv2.VideoCapture(str(ROOT/'references/season1_intro.mp4'))
if master is None or not cap.isOpened():raise RuntimeError('The master image and season1_intro.mp4 are required')
fps=cap.get(cv2.CAP_PROP_FPS);count=int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
sift=cv2.SIFT_create(nfeatures=16000,contrastThreshold=.025);k0,d0=sift.detectAndCompute(cv2.cvtColor(master,cv2.COLOR_BGR2GRAY),None);bf=cv2.BFMatcher();samples=[];brightness=[]
for index in range(count):
 ok,frame=cap.read()
 if not ok:break
 brightness.append(float(frame.mean()))
 if index%12 and index!=count-1:continue
 small=cv2.resize(frame,(1280,720));k,d=sift.detectAndCompute(cv2.cvtColor(small,cv2.COLOR_BGR2GRAY),None)
 cv2.imwrite(str(OUT/f'video_{index:03d}.jpg'),frame)
 if d is None:continue
 good=[a for a,b in bf.knnMatch(d0,d,k=2) if a.distance<.68*b.distance]
 if len(good)<8:continue
 a=np.float32([k0[m.queryIdx].pt for m in good]);b=np.float32([k[m.trainIdx].pt for m in good]);M,mask=cv2.estimateAffinePartial2D(a,b,method=cv2.RANSAC,ransacReprojThreshold=3,maxIters=10000,confidence=.999)
 yes=mask.ravel().astype(bool);a,b=a[yes],b[yes]
 # The observed camera does not rotate. Refit a common scale and XY translation.
 X=np.zeros((2*len(a),3));X[::2,0]=a[:,0];X[1::2,0]=a[:,1];X[::2,1]=1;X[1::2,2]=1
 scale,tx,ty=np.linalg.lstsq(X,b.reshape(-1),rcond=None)[0];res=(X@np.array([scale,tx,ty])-b.reshape(-1)).reshape(-1,2)
 samples.append({'frame':index+1,'time':index/fps,'scale':float(scale),'translation':[float(tx),float(ty)],'inliers':len(a),'rmse_pixels_1280':float(np.sqrt(np.mean(np.sum(res**2,axis=1))))})
cap.release()
# Fit the linear dolly/zoom segment, then its stationary title hold.
moving=[q for q in samples if q['time']<=7.0];held=[q for q in samples if 7.8<=q['time']<=10.0]
X=np.array([[q['time'],1] for q in moving]);Y=np.array([[q['scale'],*q['translation']] for q in moving]);weights=np.sqrt([q['inliers'] for q in moving]);coef=np.linalg.lstsq(X*weights[:,None],Y*weights[:,None],rcond=None)[0]
hold=np.median([[q['scale'],*q['translation']] for q in held],axis=0)
stop=float(np.median((hold-coef[1])/coef[0]));pose=coef[1]+coef[0]*stop
last_visible=max(i for i,v in enumerate(brightness) if v>3)
report={'reference':'Local season1_intro.mp4; archived original wide production still','source_fps':fps,'source_frame_count':count,'duration_seconds':count/fps,'comparison_resolution':[1280,720],'camera_model':'Fixed orthographic orientation; linearly increasing projected scale and XY translation, followed by a hold.','start':{'scale':float(coef[1,0]),'translation':coef[1,1:].tolist()},'per_second':{'scale':float(coef[0,0]),'translation':coef[0,1:].tolist()},'hold_time':stop,'end':{'scale':float(pose[0]),'translation':pose[1:].tolist()},'last_visible_frame':last_visible+1,'samples':samples,'scope':'Camera feature alignment only. This does not measure modeled-building fidelity.'}
(ROOT/'source/intro_camera.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:v for k,v in report.items() if k!='samples'},indent=2));print('CAMERA_SAMPLES',len(samples),'MEDIAN_RMSE',float(np.median([q['rmse_pixels_1280'] for q in samples])))
