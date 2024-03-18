import cv2
import time
from matplotlib import pyplot as plt
from inference_sdk import InferenceHTTPClient
import random

# 初始化客戶端
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",  # 替换成你的API地址
    api_key="8PDQPddlEJEtFa7mn7AN"  # 替换成你的API密钥
)

def is_flush(cards):
    suits = [card[1] for card in cards]
    return len(set(suits)) == 1

def is_straight(hist):
    """检查是否为顺子"""
    for i in range(9):
        if all(hist[1][i:i+5]):
            return True
    return False

def is_straight_flush(cards, hist):
    """检查是否为同花顺"""
    return is_flush(cards) and is_straight(hist)

def is_four_of_a_kind(hist):
    """检查是否为四条"""
    return 4 in hist[1]

def is_full_house(hist):
    """检查是否为葫芦"""
    return hist[1].count(3) == 1 and hist[1].count(2) == 1

def is_three_of_a_kind(hist):
    """检查是否为三条"""
    return 3 in hist[1]

def is_two_pair(hist):
    """检查是否为两对"""
    return hist[1].count(2) == 2

def is_pair(hist):
    """检查是否为一对"""
    return hist[1].count(2) == 1

def is_high_card(hist):
    """检查是否为高牌"""
    return max(hist[1]) == 1 and not is_straight(hist)

def is_royal_flush(cards, hist):
    """检查是否为皇家同花顺"""
    return is_straight_flush(cards, hist) and hist[1][9] == 1

def update_histogram_with_detection(cards, card_values):
    """更新直方图以反映检测到的扑克牌"""
    histogram = [[i for i in range(1, 14)], [0]*13]
    for card in cards:
        rank_value = card_values.get(card[:-1], 0)
        histogram[1][rank_value - 1] = 1
    return histogram

def fill_histogram_for_incomplete_hand(hist):
    """对不足五张的牌面随机补足至五张"""
    detected_cards = sum(hist[1])
    while detected_cards < 5:
        card_to_add = random.randint(0, 12)
        if hist[1][card_to_add] == 0:
            hist[1][card_to_add] = 1
            detected_cards += 1
    return hist

def infer_hand_from_image(image):
    cv2.imwrite('temp.jpg', image)
    result = CLIENT.infer('temp.jpg', model_id="playing-cards-ow27d/4")
    cards = [prediction['class'] for prediction in result['predictions']]
    if not cards:
        print("没有检测到信息")
        return

    card_values = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13}
    hist = update_histogram_with_detection(cards, card_values)
    hist = fill_histogram_for_incomplete_hand(hist)

    if is_royal_flush(cards, hist):
        print("皇家同花顺")
    elif is_straight_flush(cards, hist):
        print("同花顺")
    elif is_four_of_a_kind(hist):
        print("四条")
    elif is_full_house(hist):
        print("葫芦")
    elif is_flush(cards):
        print("同花")
    elif is_straight(hist):
        print("顺子")
    elif is_three_of_a_kind(hist):
        print("三条")
    elif is_two_pair(hist):
        print("两对")
    elif is_pair(hist):
        print("一对")
    elif is_high_card(hist):
        print("高牌")
    else:
        print("其他牌型")

cap = cv2.VideoCapture(0)
next_inference_time = time.time() + 3  # 修改为每三秒进行一次推断

try:
    plt.ion()
    figure, ax = plt.subplots(figsize=(10, 6))
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        current_time = time.time()
        if current_time >= next_inference_time:
            infer_hand_from_image(frame)
            next_inference_time = current_time + 3
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        ax.clear()
        ax.imshow(frame)
        plt.pause(0.001)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
finally:
    cap.release()
    cv2.destroyAllWindows()
    plt.ioff()
