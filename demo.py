

def get_histogram(cards, card_values):
    hist = [0] * 13
    for card in cards:
        rank = card_values[card]
        hist[rank-1] = hist[rank-1] + 1
    return hist

def is_three_of_a_kind(hist):
    return 3 in hist

def is_pair(hist):
    return pair_count(hist) == 1

def is_two_pairs(hist):
    return pair_count(hist) == 2

def pair_count(hist):
    pair_count = 0
    for count in hist:
        if count == 2:
            pair_count += 1
    return pair_count

# def is_two_paris(hist):

card_values = {'A': 1, '2': 2, '3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, '10': 10, 'J': 11, 'Q': 12, 'K': 13}

cards = ['A', 'J', 'J', 'J', 'A'] # 不同的五張牌

hist = get_histogram(cards, card_values)
print(hist)

if is_three_of_a_kind(hist):
    print('three of a kind')


if is_pair(hist):
    print('single pair')

if is_two_pairs(hist):
    print('two pairs')    