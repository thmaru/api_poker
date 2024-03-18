import cv2
import requests

# 初始化API客戶端設定
API_URL = "https://detect.roboflow.com"
API_KEY = "XREiYxq7OSKuOrd7gEAu"
MODEL_ID = "playing-cards-ow27d/4"

def is_straight(cards):
    card_values = {'A': 1, 'J': 11, 'Q': 12, 'K': 13}
    values = []
    for card in cards:
        value = card[:-1]
        value = card_values.get(value, value)
        values.append(int(value))
    values.sort()
    if values == [1, 2, 3, 4, 5]:
        return True
    if 'A' in cards:
        values = [14 if value == 1 else value for value in values]
        values.sort()
    for i in range(1, len(values)):
        if values[i] - values[i - 1] != 1:
            return False
    return len(values) == 5 and values[-1] - values[0] == 4

def infer_straight_from_frame(frame):
    _, img_encoded = cv2.imencode('.jpg', frame)
    response = requests.post(
        f"{API_URL}/{MODEL_ID}",
        files={"file": img_encoded.tobytes()},
        data={"api_key": API_KEY},
    )
    result = response.json()
    cards = [prediction['class'] for prediction in result['predictions']]
    return is_straight(cards)

def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("無法打開攝影機")
        return

    while True:
        ret, frame = cap.read()
        if not ret:
            print("無法讀取影像")
            break

        cv2.imshow('Camera Output', frame)
        
        # 每次捕捉到新的一幀時進行推論
        if cv2.waitKey(1) & 0xFF == ord('d'):  # 按 'd' 鍵進行偵測
            if infer_straight_from_frame(frame):
                print("是順子")
            else:
                print("不是順子")

        if cv2.waitKey(1) & 0xFF == ord('q'):  # 按 'q' 鍵退出
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
