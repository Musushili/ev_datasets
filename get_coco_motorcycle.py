import os
import requests
from pycocotools.coco import COCO
from tqdm import tqdm
from PIL import Image
from io import BytesIO

# COCO 数据集路径（请修改为你本地的路径）
annFile = "annotations/instances_train2017.json"
save_dir = "motorcycle_images"

# 创建保存图片的文件夹
os.makedirs(save_dir, exist_ok=True)

# 初始化 COCO API
coco = COCO(annFile)

# 获取 "motorcycle" 类别的 ID
catIds = coco.getCatIds(catNms=['motorcycle'])
if not catIds:
    print("未找到 'motorcycle' 类别，请检查类别名称。")
    exit()

# 获取所有包含 "motorcycle" 的图像 ID
imgIds = coco.getImgIds(catIds=catIds)

# 获取图像信息
imgs = coco.loadImgs(imgIds)

print(f"共找到 {len(imgs)} 张包含 'motorcycle' 的图片")

# 遍历并下载图片
for img in tqdm(imgs, desc="Downloading"):
    img_url = img['coco_url']  # COCO 提供的在线图片 URL
    img_filename = os.path.join(save_dir, img['file_name'])

    # 检查是否已下载
    if os.path.exists(img_filename):
        continue

    try:
        response = requests.get(img_url, timeout=10)
        if response.status_code == 200:
            image = Image.open(BytesIO(response.content))
            image.save(img_filename)
        else:
            print(f"下载失败: {img_url}")
    except Exception as e:
        print(f"错误: {e}")

print(f"所有图片下载完成，存储在 {save_dir} 文件夹中")
