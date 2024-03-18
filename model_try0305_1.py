import cv2
import time
import torch
from matplotlib import pyplot as plt
from torchvision import transforms

# 加載模型
model_path = 'C:\\Users\\ST\\Desktop\\Python\\best.pt'
model = torch.load(model_path)
model.eval()  # 將模型設置為評估模式

def is_straight(cards):
    """
    判斷牌面是否為順子。
    """
    card_values = {'A': 14, 'J': 11, 'Q': 12, 'K': 13, '10': 10, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}
    values = [card_values[card[:-1]] for card in cards]
    values.sort()

    if len(values) < 5:
        return False

    special_straight = {10, 11, 12, 13, 14}
    if set(values) == special_straight:
        return True

    for i in range(len(values) - 4):
        if values[i+4] - values[i] == 4:
            return True
    return False

def infer_straight_from_image(image):
    """
    使用本地模型推論影像並判斷是否為順子。
    """
    transform = transforms.Compose([
        transforms.ToPILImage(),
        transforms.Resize((640, 640)),
        transforms.ToTensor(),
    ])
    image_tensor = transform(image).unsqueeze(0)  # 添加一個批次維度

    with torch.no_grad():
        predictions = model(image_tensor)

    # 處理預測結果...
    # 這裡需要根據你的模型輸出格式來提取和轉換預測結果
    # 下面是一個假設的例子，實際上可能需要調整
    cards = [prediction['class'] for prediction in predictions[0]]
    print(cards)
    if is_straight(cards):
        print("是順子")
    else:
        print("不是順子")

# 初始化攝影機等後續代碼保持不變...
