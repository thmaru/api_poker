import cv2
from inference_sdk import InferenceHTTPClient
import random

# 初始化客户端
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",  # 替换成你的API地址
    api_key="8PDQPddlEJEtFa7mn7AN"  # 替换成你的API密钥
)

def get_histogram_and_suits(cards, card_values):
    hist = [0] * 13  # 牌值直方图
    suits = {'S': 0, 'H': 0, 'D': 0, 'C': 0}  # 花色计数
    for card in cards:
        value, suit = card[:-1], card[-1]  # 分割牌的值和花色
        if value in card_values:
            rank = card_values[value]
            hist[rank-1] += 1
            suits[suit] += 1
    return hist, suits

def is_flush(suits):
    # 检查是否为同花
    return any(count >= 5 for count in suits.values())

def is_straight(hist):
    for i in range(9):
        if all(hist[i:i+5]):
            return True
    return False

def is_straight_flush(cards, hist, suits):
    return is_flush(suits) and is_straight(hist)

def is_four_of_a_kind(hist):
    return 4 in hist

def is_full_house(hist):
    return 3 in hist and 2 in hist

def is_three_of_a_kind(hist):
    return 3 in hist

def is_two_pair(hist):
    pairs = [count for count in hist if count == 2]
    return len(pairs) == 2

def is_pair(hist):
    return hist.count(2) == 1

def is_high_card(hist):
    return max(hist) == 1 and not is_straight(hist)

def infer_hand_from_image(image_path):
    image = cv2.imread(image_path)
    cv2.imwrite('temp.jpg', image)
    result = CLIENT.infer('temp.jpg', model_id="playing-cards-ow27d/4")
    cards = [prediction['class'] for prediction in result['predictions']]
    
    print("检测到的牌面:", cards)
    
    if not cards:
        print("没有检测到信息")
        return

    card_values = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13}
    hist, suits = get_histogram_and_suits(cards, card_values)

    if is_straight_flush(cards, hist, suits):
        print("同花顺")
    elif is_four_of_a_kind(hist):
        print("四条")
    elif is_full_house(hist):
        print("葫芦")
    elif is_flush(suits):
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

# 使用示例
image_path = "C:/Users/ST/Desktop/Python/10.jpg"  # 替换成你的图片路径
infer_hand_from_image(image_path)
