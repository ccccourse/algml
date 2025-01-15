from ultralytics import YOLO

# Create a new YOLO model from scratch
model = YOLO("yolo11n.yaml")

# Load a pretrained YOLO model (recommended for training)
model = YOLO("yolo11n.pt")

# Perform object detection on an image using the model
results = model("https://ultralytics.com/images/bus.jpg")
print('results=', results)
