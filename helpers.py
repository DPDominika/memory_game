import os


START_POINT = 5
SCORE_LINE = 20


def get_cards():
    directory = "resources/images/"
    card_list = []
    for file in os.listdir(directory):
        if os.path.splitext(file)[1] == '.jpg' and os.path.splitext(file)[0].startswith("img"):
            card_list.append(os.path.join(file))
            card_list.sort()
    return card_list


def calc_all_divisors(card_list):
    cards_amount = len(card_list)*2
    all_divisors = []
    for i in range(1, cards_amount + 1):
        if cards_amount % i == 0:
            all_divisors.append((cards_amount // i))
    return all_divisors


def calc_pair_divisors(all_divisors):
    size = len(all_divisors)
    if size % 2 == 0:
        return all_divisors[size // 2-1: size // 2+1]
    else:
        return all_divisors[size // 2]


def calc_board_columns(col_rows):
    if type(col_rows) == int:
        return col_rows
    return max(col_rows)


def calc_board_rows(col_rows):
    if type(col_rows) == int:
        return col_rows
    return min(col_rows)


def calc_card_size(card_list):
    if len(card_list) <= 9:
        return 200
    return 100


def calc_board_size_pixels():
    card_list = get_cards()
    card_size = calc_card_size(card_list)
    all_divisors = calc_all_divisors(card_list)
    col_rows = calc_pair_divisors(all_divisors)
    display_width = calc_board_columns(col_rows) * card_size + ((calc_board_columns(col_rows)+1) * START_POINT)
    display_height = calc_board_rows(col_rows) * card_size + ((calc_board_rows(col_rows)+1) * START_POINT + SCORE_LINE)
    return display_width, display_height

card_list = get_cards()
print(calc_all_divisors(card_list))