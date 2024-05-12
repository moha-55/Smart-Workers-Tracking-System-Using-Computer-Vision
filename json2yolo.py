import json
import os
from pathlib import Path
from tqdm import tqdm
import yaml

def convert(json_dir):
    # Convert JSON labels to YOLO labels
    class_mapping = {"squat": 0, "run": 1, "sit": 2, "stretch": 3, "walk": 4, "jump": 5, "bendover": 6, "stand": 7, "lying": 8}
    names = list(class_mapping.keys())  # class names

    # Create directories for YOLO labels
    save_dir = Path(json_dir).parent / 'labels'
    save_dir.mkdir(parents=True, exist_ok=True)

    # Loop through JSON files in the specified directory
    for json_file in tqdm(list(Path(json_dir).glob('*.json')), desc='Converting JSON to YOLO'):
        with open(json_file) as f:
            data = json.load(f)  # Load JSON

        # Create label file path
        label_path = save_dir / Path(json_file.stem).with_suffix('.txt').name

        for person in data['persons']:
            # Box
            xmin, ymin, ymax, xmax = person['bndbox'].values()
            width = xmax - xmin
            height = ymax - ymin
            xywh = [(xmin + width / 2) / data['width'], (ymin + height / 2) / data['height'], width / data['width'], height / data['height']]

            # Class
            cls = list(person['actions'].keys())[list(person['actions'].values()).index(1)]  # Extract class with value 1
            class_index = class_mapping[cls]

            line = class_index, *xywh  # YOLO format (class_index, xywh)
            with open(label_path, 'a') as f:
                f.write(('%g ' * len(line)).rstrip() % line + '\n')

    # Save dataset.yaml
    d = {'path': f"{str(Path(json_dir).parent)}",  # dataset root dir
         'train': "labels  # train labels (relative to path)",
         'val': "",  # leave empty for now
         'test': "",  # leave empty for now
         'nc': len(names),
         'names': names}  # dictionary

    with open(save_dir.parent / 'dataset.yaml', 'w') as f:
        yaml.dump(d, f, sort_keys=False)

    print('Conversion completed successfully!')

if __name__ == '__main__':
    convert('M:/sem8/FYP2/POLAR/hvnsh7rwz7-1/Annotations/annotations')
