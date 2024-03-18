import cv2
import time
from matplotlib import pyplot as plt
from inference_sdk import InferenceHTTPClient

# 初始化客戶端
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="8PDQPddlEJEtFa7mn7AN"
)

def is_straight(cards):
    """
    判斷牌面是否為順子。
    """
    card_values = {'A': 14, 'J': 11, 'Q': 12, 'K': 13, '10': 10, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9}
    values = [card_values[card[:-1]] for card in cards]  # 移除牌面的花色信息並轉換值
    values.sort()

    # 牌數不足五張視為不是順子
    if len(values) < 5:
        return False

    # 檢查順子（包括特殊順子）
    special_straight = {10, 11, 12, 13, 14}  # 特殊順子的值集合
    if set(values) == special_straight:
        return True

    for i in range(len(values) - 4):
        if values[i+4] - values[i] == 4:
            return True  # 是順子
    return False  # 不是順子

def infer_straight_from_image(image):
    """
    使用模型推論影像並判斷是否為順子。
    """
    cv2.imwrite('temp.jpg', image)  # 保存臨時文件
    result = CLIENT.infer('temp.jpg', model_id="playing-cards-ow27d/4")
    cards = [prediction['class'] for prediction in result['predictions']]
    if not cards:
        print("沒有偵測到資訊")
        return

    print(cards)
    if is_straight(cards):
        print("是順子")
    else:
        print("不是順子")

# 初始化攝影機
cap = cv2.VideoCapture(0)  # 0 是預設的攝影機ID

# 設置下次推論的時間
next_inference_time = time.time() + 1  # 從現在開始的一秒後

try:
    plt.ion()  # 啟用互動模式
    figure, ax = plt.subplots(figsize=(10, 6))  # 創建繪圖對象和軸
    while True:
        # 捕捉幀
        ret, frame = cap.read()
        if not ret:
            break

        # 當前時間
        current_time = time.time()

        # 如果達到下次推論時間，進行推論並更新下次推論時間
        if current_time >= next_inference_time:
            infer_straight_from_image(frame)
            next_inference_time = current_time + 1  # 設置下一次推論的時間

        # 將圖像從 BGR 轉換為 RGB
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        ax.clear()  # 清除之前的圖像
        ax.imshow(frame)  # 顯示新的幀
        plt.pause(0.001)  # 暫停一下以便更新

        # 按 'q' 退出（這部分需要在圖形界面上操作）
        if plt.waitforbuttonpress(0.001):
            break
finally:
    cap.release()
    plt.ioff
