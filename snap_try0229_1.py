import cv2
import time
import os
from matplotlib import pyplot as plt
from inference_sdk import InferenceHTTPClient

# 確保儲存截圖的目錄存在
snapshot_dir = "C:\\poker_snap"
if not os.path.exists(snapshot_dir):
    os.makedirs(snapshot_dir)

# 初始化客戶端
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="XREiYxq7OSKuOrd7gEAu"
)

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
    使用模型推論影像並判斷是否為順子。
    """
    cv2.imwrite('temp.jpg', image)
    result = CLIENT.infer('temp.jpg', model_id="playing-cards-ow27d/4")
    cards = [prediction['class'] for prediction in result['predictions']]
    if not cards:
        print("沒有偵測到資訊")
        return False

    print(cards)
    return is_straight(cards)

# 初始化攝影機
cap = cv2.VideoCapture(0)

plt.ion()
figure, ax = plt.subplots(figsize=(10, 6))

try:
    next_inference_time = time.time() + 1
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        current_time = time.time()
        if current_time >= next_inference_time:
            if infer_straight_from_image(frame):
                print("是順子，正在儲存截圖...")
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                snapshot_path = os.path.join(snapshot_dir, f"straight_{timestamp}.jpg")
                cv2.imwrite(snapshot_path, frame)
                print(f"截圖已儲存到 {snapshot_path}")
            next_inference_time = current_time + 1

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        ax.clear()
        ax.imshow(frame)
        plt.pause(0.001)

        if plt.waitforbuttonpress(0.001):
            break
except Exception as e:
    print(f"發生錯誤: {e}")
finally:
    cap.release()
    plt.ioff()
    plt.close()
