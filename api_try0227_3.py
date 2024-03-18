# 直接定義10,J,Q,K,A為特殊情況的順子
from inference_sdk import InferenceHTTPClient

# 初始化客户端
CLIENT = InferenceHTTPClient(
    api_url="https://detect.roboflow.com",
    api_key="XREiYxq7OSKuOrd7gEAu"
)

def is_straight(cards):
    """
    判断牌面是否为顺子。
    """
    if not cards:  # 如果牌面列表为空，直接返回False
        return False

    # 将牌面转换为排序后的数字列表
    card_values = {'A': 1, 'J': 11, 'Q': 12, 'K': 13, '10': 10}
    values = []
    for card in cards:
        # 提取牌面的值（去除花色）
        value = card[:-1]
        # 转换J, Q, K, A, 10为对应的数字
        value = card_values.get(value, value)
        values.append(int(value))
    values.sort()

    # 特殊情况：直接检查是否包含 "10,J,Q,K,A"
    if set(values) == {10, 11, 12, 13, 1}:
        return True

    # 检查是否为一般顺子
    for i in range(1, len(values)):
        if values[i] - values[i - 1] != 1:
            return False
    return True

def infer_straight(image_path):
    """
    使用模型推断图片并判断是否为顺子。
    """
    # 调用API进行图片推断
    result = CLIENT.infer(image_path, model_id="playing-cards-ow27d/4")
    # 解析结果中的牌面标签
    cards = [prediction['class'] for prediction in result['predictions']]
    print(cards)
    # 判断是否为顺子
    if is_straight(cards):
        print("是顺子")
    else:
        print("不是顺子")

# 使用示例
infer_straight("3.jpg")


