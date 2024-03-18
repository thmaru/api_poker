def get_histogram_and_suits(cards):
    hist = [0] * 13  # 牌值直方图
    suits = {'S': 0, 'H': 0, 'D': 0, 'C': 0}  # 花色计数
    for card in cards:
        value, suit = card[:-1], card[-1]  # 分割牌的值和花色
        if value == '10':  # 特殊处理10
            value = 'T'
        rank = '23456789TJQKA'.index(value)
        hist[rank] += 1
        suits[suit] += 1
    return hist, suits

def is_flush(suits):
    return any(count >= 5 for count in suits.values())

def is_straight(hist):
    for i in range(9):
        if all(hist[i:i+5]):
            return True
    # 检查A2345的特殊情况
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
    pairs = [count for count in hist if count == 2]
    return len(pairs) == 2

def is_pair(hist):
    return hist.count(2) == 1

def is_royal_flush(hist, suits):
    return is_straight_flush(hist, suits) and hist[9] == 1  # 检查10, J, Q, K, A都存在

def infer_hand_from_cards(cards):
    print("输入的牌面:", cards)
    
    hist, suits = get_histogram_and_suits(cards)

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

# 使用示例
# cards_input = ['2H', '3C', 'QS', 'AD', 'QH']  # 示例输入
cards_input = ['4H', '4C', '4S']  # 示例输入
infer_hand_from_cards(cards_input)
