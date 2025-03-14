import json

# 1. 读取原始 COCO 标注文件
with open("annotation.json", "r") as f:
    coco_data = json.load(f)

# 2. 获取所有带目标的图片 ID
annotated_image_ids = set(ann["image_id"] for ann in coco_data["annotations"])

# 3. 筛选出仅包含有目标的图片
filtered_images = [img for img in coco_data["images"] if img["id"] in annotated_image_ids]

# 4. 生成新的 COCO 标注数据（去除负样本）
filtered_coco_data = {
    "images": filtered_images,
    "annotations": coco_data["annotations"],
    "categories": coco_data["categories"],
    "info": coco_data["info"],
    "licenses": coco_data["licenses"]
}

# 5. 保存新的标注文件
with open("annotation_no_neg.json", "w") as f:
    json.dump(filtered_coco_data, f, indent=4)

print(f"生成 annotation_no_neg.json，原始图片数量：{len(coco_data['images'])}，去除后图片数量：{len(filtered_images)}")
