#!/usr/bin/env python3
"""Prepare a user portrait for ASCII conversion. Requires Pillow, OpenCV and rembg."""
import sys,os
import cv2,numpy as np
from PIL import Image
from rembg import remove
HERE=os.path.dirname(os.path.abspath(__file__))
src=sys.argv[1] if len(sys.argv)>1 else os.path.join(HERE,"..","source-photo.jpg")
dst=sys.argv[2] if len(sys.argv)>2 else os.path.join(HERE,"..","source-prepped.png")
cut=remove(Image.open(src).convert("RGBA"))
rgb=np.array(cut.convert("RGB")); alpha=np.array(cut.split()[-1])
gray=cv2.cvtColor(rgb,cv2.COLOR_RGB2GRAY)
smooth=cv2.bilateralFilter(gray,9,40,9)
fg=smooth[alpha>128]
lo,hi=np.percentile(fg,[2,92]); tone=np.clip((smooth.astype(np.float32)-lo)/(hi-lo),0,1)*255
mask=cv2.GaussianBlur(alpha.astype(np.float32)/255,(0,0),1)
out=tone*mask+255*(1-mask)
ys,xs=np.where(alpha>20); side=max(xs.max()-xs.min(),ys.max()-ys.min())+60
cx,cy=(xs.min()+xs.max())//2,(ys.min()+ys.max())//2
canvas=np.full((side,side),255,np.uint8); x0,y0=cx-side//2,cy-side//2
sx0,sy0=max(x0,0),max(y0,0); sx1,sy1=min(x0+side,out.shape[1]),min(y0+side,out.shape[0])
canvas[sy0-y0:sy1-y0,sx0-x0:sx1-x0]=out[sy0:sy1,sx0:sx1].astype(np.uint8)
Image.fromarray(canvas).save(dst); print("Wrote",dst)
