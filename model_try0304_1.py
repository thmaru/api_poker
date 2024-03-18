import cv2
import time
import argparse
import torch
from matplotlib import pyplot as plt
from torchvision import transforms
from models.my_model import MyModelClass
import sys

sys.path.append('C:/Users/ST/Desktop/Python/')

# 加載本地模型
# model_path = "C:/Users/ST/Desktop/Python/best.pt"
model_path = "best.pt"
model.load_state_dict(torch.load(model_path))
model.eval()  # 將模型設置為評估模式

def infer_straight_from_image(image):
    """
    使用本地模型推論影像並判斷是否為順子。
    """
    # 將 OpenCV 圖像轉換為 PyTorch 張量
    transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((256, 256)),
        transforms.ToTensor(),
    ])
    image_tensor = transform(image)
    image_tensor = image_tensor.unsqueeze(0)  # 增加一個批次維度

    # 使用模型進行推論
    with torch.no_grad():
        result = model(image_tensor)
    
    # 這裡你需要根據實際模型的輸出格式來解析結果
    # 例如：cards = 解析 result 來獲得卡片標籤
    # 下面的 cards 變量和 is_straight 函數的調用需要根據實際情況進行調整
    cards = []  # 假設這裡是從模型輸出解析出的卡片標籤列表
    
    print(cards)
    if is_straight(cards):
        print("是順子")
    else:
        print("不是順子")

# 以下初始化攝影機和循環讀取影像的代碼保持不變
# if __name__ == '__main__':
#     parser = argparse.ArgumentParser()
#     parser.add_argument('--weights', nargs='+', type=str, default=r'C:/yolov7/runs/train/exp/weights/best.pt', help='model.pt path(s)')