import cv2
from inference_sdk import InferenceHTTPClient

# 初始化客户端
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",  # 替换成你的API地址
    api_key="8PDQPddlEJEtFa7mn7AN"  # 使用您的API密钥
)

def get_histogram_and_suits(cards):
    hist = [0] * 13  # 牌值直方图
    suits = {'S': 0, 'H': 0, 'D': 0, 'C': 0}  # 花色计数
    for card in cards:
        value, suit = card[:-1], card[-1]
        if value == '10':  # 特殊处理10
            value = 'T'
        rank = '23456789TJQKA'.index(value)
        hist[rank] += 1
        suits[suit] += 1
    return hist, suits

def infer_hand_from_image(image):
    cv2.imwrite('temp.jpg', image)
    result = CLIENT.infer('temp.jpg', model_id="playing-cards-ow27d/4")
    cards = [prediction['class'] for prediction in result['predictions']]
    
    print("检测到的牌面:", cards)
    
    if not cards:
        print("没有检测到信息")
        return
    
    hist, suits = get_histogram_and_suits(cards)
    print_determine_hand_type(hist, suits)

def capture_and_process():
    cap = cv2.VideoCapture(0)
    print("按下空白键进行辨识偵測，按下'q'退出...")
    while True:
        ret, frame = cap.read()
        cv2.imshow("Camera", frame)
        key = cv2.waitKey(1)
        if key & 0xFF == ord('q'):  # 按'q'退出
            break
        elif key & 0xFF == ord(' '):  # 按下空白键拍照并辨识
            infer_hand_from_image(frame)

    cap.release()
    cv2.destroyAllWindows()

# 以下是您提供的牌型判断函数
def is_flush(suits):
    return any(count >= 5 for count in suits.values())

def is_straight(hist):
    for i in range(9):
        if all(hist[i:i+5]):
            return True
    if all(hist[i] for i in [0, 12, 1, 2, 3]):
        return True
    return False

def is_straight_flush(hist, suits):
    return is_flush(suits) and is_straight(hist)

def is_four_of_a_kind(hist):
    return 4 in hist

def is_full_house(hist):
    return 3 in hist and 2 in hist

def is_three_of_a_kind(hist):
    return 3 in hist

def is_two_pair(hist):
    return hist.count(2) == 2

def is_pair(hist):
    return hist.count(2) == 1

def is_royal_flush(hist, suits):
    return is_straight_flush(hist, suits) and hist[9] == 1

def print_determine_hand_type(hist, suits):
    if is_royal_flush(hist, suits):
        print("皇家同花顺")
    elif is_straight_flush(hist, suits):
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
    else:
        print("高牌")

if __name__ == "__main__":
    capture_and_process()
