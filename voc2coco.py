import os
import xml.etree.ElementTree as ET
import json
from tqdm import tqdm

def voc_to_coco():
    # 输入输出路径配置
    images_dir = r'C:\Users\Winona.Shao\GP\ev_datasets\ev\images'
    xml_dir = r'C:\Users\Winona.Shao\GP\ev_datasets\ev\xml'
    output_dir = r'C:\Users\Winona.Shao\GP\ev_datasets\ev\annotations'
    os.makedirs(output_dir, exist_ok=True)
    output_json = os.path.join(output_dir, 'annotation.json')

    # 初始化COCO数据结构
    coco = {
        "info": {
            "description": "EV Dataset",
            "version": "1.0",
            "year": 2023,
            "contributor": "",
            "url": ""
        },
        "licenses": [],
        "categories": [
            {"id": 1, "name": "motorcycle", "supercategory": ""},
            {"id": 2, "name": "bike", "supercategory": ""}
        ],
        "images": [],
        "annotations": []
    }

    # 类别映射字典
    category_mapping = {
        "motorcycle": "motorcycle",
        "bike": "bike"
    }

    # 创建类别ID映射
    category_ids = {cat["name"]: cat["id"] for cat in coco["categories"]}

    annotation_id = 1

    # 遍历所有XML文件
    for xml_file in tqdm(os.listdir(xml_dir)):
        if not xml_file.endswith('.xml'):
            continue

        xml_path = os.path.join(xml_dir, xml_file)
        tree = ET.parse(xml_path)
        root = tree.getroot()

        # 解析图像信息
        filename = root.find('filename').text
        image_path = os.path.join(images_dir, filename)
        
        if not os.path.exists(image_path):
            print(f"Warning: Image {image_path} not found, skipping...")
            continue

        size = root.find('size')
        width = int(size.find('width').text)
        height = int(size.find('height').text)

        # 添加图像信息
        image_id = len(coco["images"]) + 1
        coco["images"].append({
            "id": image_id,
            "file_name": filename,
            "width": width,
            "height": height
        })

        # 处理每个标注对象
        for obj in root.findall('object'):
            original_name = obj.find('name').text
            # 转换类别名称
            coco_name = category_mapping.get(original_name)
            
            if not coco_name:
                continue

            # 获取类别ID
            category_id = category_ids[coco_name]

            # 解析边界框
            bndbox = obj.find('bndbox')
            xmin = int(bndbox.find('xmin').text)
            ymin = int(bndbox.find('ymin').text)
            xmax = int(bndbox.find('xmax').text)
            ymax = int(bndbox.find('ymax').text)

            # 转换为COCO格式的bbox
            width_box = xmax - xmin
            height_box = ymax - ymin

            # 添加标注信息
            coco["annotations"].append({
                "id": annotation_id,
                "image_id": image_id,
                "category_id": category_id,
                "bbox": [xmin, ymin, width_box, height_box],
                "area": width_box * height_box,
                "iscrowd": 0,
                "segmentation": []
            })
            annotation_id += 1

    # 保存为JSON文件
    with open(output_json, 'w') as f:
        json.dump(coco, f, indent=2)
    print(f"Conversion completed! Saved to {output_json}")

if __name__ == '__main__':
    voc_to_coco()