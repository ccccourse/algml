from ultralytics import YOLO

model = YOLO("yolo11n.pt")
# accepts all formats - image/dir/Path/URL/video/PIL/ndarray. 0 for webcam
results = model.predict(source="0") # 直接抓相機鏡頭辨識結果，不斷循環
