from random import shuffle
from datetime import datetime
import helpers as helper


card_list = helper.get_cards()
all_divisors = helper.calc_all_divisors(card_list)
unique_divisors = helper.calc_pair_divisors(all_divisors)

def build_row(columns):
    list_a = []
    for number in range(columns):
        list_a.append(None)
    return list_a


def build_rows(rows, columns):
    rows_a = []
    for i in range(rows):
        row = build_row(columns)
        rows_a.append(row)
    return rows_a


def make_empty_board(rows, columns):
    """Buduje pustą plansze do gry, pola wypełnione 'None' """
    return build_rows(rows, columns)


def cards_indexes(columns):
    """zwraca listę ze wszystkimi indeksami kart"""
    indexes = []
    board_rows = helper.calc_board_rows(unique_divisors) * helper.calc_board_columns(unique_divisors)
    for i in range(board_rows):
        indexes.append(divmod(i, columns))
    return indexes


def random_cards_indexes(indexes):
    """zwraca listę z losowo ułożonymi indeksami wszystkich kart"""
    shuffle(indexes)
    return indexes


def create_card(value):
    return {'value': value, 'showed': False}


def create_cards():
    values = list(range(len(card_list))) * 2
    cards = []
    for value in values:
        cards.append(create_card(value))
    return cards


def make_game_board(board, random_indexes, cards):
    """wstawia karty na planszę. (Karty są zakryte, gra się zaczyna)"""
    count = 0
    for x, y in random_indexes:
        board[x][y] = cards[count]
        count += 1
    return board


def run_board_default():
    """Zwraca planaszę, gotową do gry, karty zakryte, ułożone losowo"""
    columns = helper.calc_board_columns(unique_divisors)
    rows = helper.calc_board_rows(unique_divisors)
    board = make_empty_board(rows, columns)
    indexes = cards_indexes(columns)
    random_indexes = random_cards_indexes(indexes)
    cards = create_cards()
    return make_game_board(board, random_indexes, cards)


def create_game(board):
    """Tworzy słownik"""
    return {'board': board,
    'active_card_indexes': None,
    'started_at': None,
    'finish_at': None,
    'attempts': 0}


def is_first_turn(game):
    if game['active_card_indexes'] is not None and len(game['active_card_indexes']) == 1:
        return False
    elif game['active_card_indexes'] is None or len(game['active_card_indexes']) == 2:
        return True


def card_showed(game, row, col):
    """Zwraca prawdę jeżeli karta jest odkryta"""
    if game['board'][row][col]['showed']:
        return True
    return False


def if_first_round(game):
    """Zwraca prawdę jężeli zaczyna się pierwsza runda gry"""
    return game['active_card_indexes'] == None


def if_first_turn_in_round(game):
    """Zwraca prawdę jeżeli gracz chce odkryć pierwszą kartę w danej rundzie """
    return len(game['active_card_indexes']) == 2


def if_second_turn_in_round(game):
    """Zwraca prawdę jeżeli gracz chce odkryć drugą kartę w danej rundzie """
    return len(game['active_card_indexes']) == 1


def get_active_card_1(game, board):
    """Zwraca pierwszą kartę wybraną przez gracza"""
    return board[game['active_card_indexes'][0][0]][game['active_card_indexes'][0][1]]


def get_active_card_2(game, board):
    """Zwraca drudą kartę wybraną przez gracza"""
    return board[game['active_card_indexes'][1][0]][game['active_card_indexes'][1][1]]


def if_equals_cards(card_1, card_2):
    """Zwraca prawdę, jeżeli dwie wybrane przez gracza karty są takie same"""
    return card_1 == card_2


def first_chosen_card(game, board):
    """Zwraca wartość pierwszej wybranej karty w rundzie"""
    x_card_1 = game['active_card_indexes'][0][0]
    y_card_1 = game['active_card_indexes'][0][1]
    return board[x_card_1][y_card_1]


def second_chosen_card(game, board):
    """Zwraca wartość drugiej wybranej karty w rundzie"""
    x_card_2 = game['active_card_indexes'][1][0]
    y_card_2 = game['active_card_indexes'][1][1]
    return board[x_card_2][y_card_2]


def equals_cards(game, board):
    """Sprawdza czy dwie wybrane karty przez gracza są takie same, jeżeli tak, zostają widoczne, jeżeli nie, są zakrywane"""
    card_1 = get_active_card_1(game, board)
    card_2 = get_active_card_2(game, board)
    if if_equals_cards(card_1, card_2):
        first_chosen_card(game, board)['showed'] = True
        second_chosen_card(game, board)['showed'] = True
    elif not if_equals_cards(card_1, card_2):
        first_chosen_card(game, board)['showed'] = False
        second_chosen_card(game, board)['showed'] = False


def first_turn(game, board, row, col):
    if if_first_round(game):
        if not card_showed(game, row, col):
            game['board'][row][col]['showed'] = True
            game['active_card_indexes'] = [(row, col)]
            game['started_at'] = datetime.now()
    elif if_first_turn_in_round(game):
        equals_cards(game, board)
        if not card_showed(game, row, col):
            game['board'][row][col]['showed'] = True
            game['active_card_indexes'] = [(row, col)]


def second_turn(game, row, col):
    if if_second_turn_in_round(game):
        if not card_showed(game, row, col):
            game['board'][row][col]['showed'] = True
            game['attempts'] += 1
            game['active_card_indexes'].append((row, col))


def on_card_clicked(game, board, columns, rows, row, col):
    """Zwraca kliknięty obrazek"""
    if is_first_turn(game):
        first_turn(game, board, row, col)
    else:
        second_turn(game, row, col)

    if all_card_showed(game, columns, rows):
        finish_game(game, columns, rows)
    return game


def count_showed_cards(game):
    """liczy ile kart odkrytych"""
    check_showed_card = 0
    for row in game['board']:
        for field in row:
            if field['showed'] == True:
                check_showed_card += 1
    return check_showed_card


def all_card_showed(game, columns, rows):
    """Sprawdza czy wszystkie karty są już odsłonięte"""
    if count_showed_cards(game) == columns * rows:
        return True
    return False


def finish_game(game, columns, rows):
    """zwraca godzinę, w której gra się zakończyła - wszystkie karty zostały odkryte"""
    if all_card_showed(game, columns, rows):
        game['finish_at'] = datetime.now()
    else:
        pass








