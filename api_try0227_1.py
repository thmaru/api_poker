from inference_sdk import InferenceHTTPClient

# 初始化客戶端
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="XREiYxq7OSKuOrd7gEAu"
)

def is_straight(cards):
    """
    判斷牌面是否為順子。
    """
    # 將牌面轉換為排序後的數字列表
    card_values = {'A': 1, 'J': 11, 'Q': 12, 'K': 13}
    values = []
    for card in cards:
        # 提取牌面的值（去除花色）
        value = card[:-1]
        # 轉換J, Q, K, A為對應的數字
        value = card_values.get(value, value)
        values.append(int(value))
    values.sort()

    # 檢查是否為順子
    for i in range(1, len(values)):
        if values[i] - values[i - 1] != 1:
            return False
    return True

def infer_straight(image_path):
    """
    使用模型推論圖片並判斷是否為順子。
    """
    # 調用API進行圖片推論
    result = CLIENT.infer(image_path, model_id="playing-cards-ow27d/4")
    # 解析結果中的牌面標籤
    cards = [prediction['class'] for prediction in result['predictions']]
    print(cards)
    # 判斷是否為順子
    if is_straight(cards):
        print("是順子")
    else:
        print("不是順子")
    
# 使用範例
infer_straight("4.jpg")