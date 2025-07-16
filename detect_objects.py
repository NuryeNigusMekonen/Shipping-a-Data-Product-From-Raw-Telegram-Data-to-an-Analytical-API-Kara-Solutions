import os
from pathlib import Path
import pandas as pd
from ultralytics import YOLO

# Define base directory for images
BASE_IMAGE_DIR = Path("data/raw/telegram_media")

# Output CSV path
OUTPUT_CSV = Path("data/processed/detections.csv")

def find_all_images(base_dir):
    # Find all jpg/jpeg/png files recursively
    img_extensions = [".jpg", ".jpeg", ".png"]
    return [p for p in base_dir.rglob("*") if p.suffix.lower() in img_extensions]

def main():
    # Load pretrained YOLOv8 model (default is 'yolov8n.pt', lightweight)
    model = YOLO('yolov8n.pt')
    # Find all images
    images = find_all_images(BASE_IMAGE_DIR)
    print(f"Found {len(images)} images to process.")
    results_data = []

    # Process each image
    for img_path in images:
        # Run detection on image, verbose=False to reduce output
        results = model(img_path, verbose=False)
        
        # Each result corresponds to one image (only one here)
        detections = results[0]

        # Extract message_id from filename (filename without extension)
        try:
            message_id = int(img_path.stem)
        except Exception:
            message_id = None

        # Iterate detected objects
        for det in detections.boxes.data.cpu().numpy():
            # det array format: [x1, y1, x2, y2, confidence, class]
            confidence = det[4]
            class_id = int(det[5])

            # Get class name from model.names dictionary
            class_name = model.names[class_id]

            results_data.append({
                "image_path": str(img_path),
                "message_id": message_id,
                "detected_object_class": class_name,
                "confidence_score": float(confidence)
            })

    # Convert results to DataFrame
    df = pd.DataFrame(results_data)

    # Make sure output directory exists
    OUTPUT_CSV.parent.mkdir(parents=True, exist_ok=True)

    # Save results to CSV
    df.to_csv(OUTPUT_CSV, index=False)

    print(f"Saved {len(df)} detections to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
