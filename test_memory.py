from memory_engine import (
    run_board_default, create_game, on_card_clicked,
    count_showed_cards, all_card_showed, create_cards,
    make_game_board, cards_indexes, make_empty_board,
    calc_pair_count, calc_board_lenght, calc_board_size,
    calc_pair_divisors, calc_all_divisors
)
import time

#         [{'value': 0, 'showed': False}, {'value': 1, 'showed': False}, {'value': 2, 'showed': False}, {'value': 3, 'showed': False}],
#         [{'value': 4, 'showed': False}, {'value': 5, 'showed': False}, {'value': 0, 'showed': False}, {'value': 1, 'showed': False}],
#         [{'value': 2, 'showed': False}, {'value': 3, 'showed': False}, {'value': 4, 'showed': False}, {'value': 5, 'showed': False}],


def make_test_board():
    pair_count = calc_pair_count()
    cards = create_cards(pair_count)
    all_divisors = calc_all_divisors(pair_count)
    unique_divisors = calc_pair_divisors(all_divisors)
    lenght = calc_board_lenght(unique_divisors)
    size = calc_board_size(unique_divisors)
    indexes = cards_indexes(lenght, unique_divisors)
    board = make_empty_board(size, lenght)
    make_game_board(board, indexes, cards)
    return board


def test_calc_board_size():
    pair_count = calc_pair_count()
    all_divisors = calc_all_divisors(pair_count)
    unique_divisors = calc_pair_divisors(all_divisors)
    assert (calc_board_lenght(unique_divisors) * calc_board_size(unique_divisors) == len(pair_count)*2)


def test_click_good_pair():
    """test sprawdza czy będą widoczne dwie poprawnie odsłonięte karty"""
    pair_count = calc_pair_count()
    all_divisors = calc_all_divisors(pair_count)
    unique_divisors = calc_pair_divisors(all_divisors)
    lenght = calc_board_lenght(unique_divisors)
    size = calc_board_size(unique_divisors)
    board = make_test_board()
    game = create_game(board)
    on_card_clicked(game, board, lenght, size, row=1, col=1)
    assert count_showed_cards(game) == 1
    on_card_clicked(game, board, lenght, size, row=2, col=3)
    assert count_showed_cards(game) == 2
    on_card_clicked(game, board, lenght, size, row=0, col=0)
    assert count_showed_cards(game) == 3
    on_card_clicked(game, board, lenght, size, row=1, col=2)
    assert count_showed_cards(game) == 4


def test_click_same_pair():
    """test sprawdza ile kart będzie odkrytych jeżeli gracz spróbuje odsłonić tą samą kartę"""
    pair_count = calc_pair_count()
    all_divisors = calc_all_divisors(pair_count)
    unique_divisors = calc_pair_divisors(all_divisors)
    lenght = calc_board_lenght(unique_divisors)
    size = calc_board_size(unique_divisors)
    board = make_test_board()
    game = create_game(board)
    on_card_clicked(game, board, lenght, size, row=1, col=1)
    assert count_showed_cards(game) == 1
    on_card_clicked(game, board, lenght, size, row=1, col=1)
    assert count_showed_cards(game) == 1


def test_if_game_is_finished():
    """test sprawdza czy po odklikaniu wszystkich par, wszystkie karty są odsłonięte"""
    pair_count = calc_pair_count()
    all_divisors = calc_all_divisors(pair_count)
    unique_divisors = calc_pair_divisors(all_divisors)
    lenght = calc_board_lenght(unique_divisors)
    size = calc_board_size(unique_divisors)
    board = make_test_board()
    game = create_game(board)
    on_card_clicked(game, board, lenght, size, row=0, col=0)
    on_card_clicked(game, board, lenght, size, row=1, col=2)
    on_card_clicked(game, board, lenght, size, row=0, col=1)
    on_card_clicked(game, board, lenght, size, row=1, col=3)
    on_card_clicked(game, board, lenght, size, row=0, col=2)
    on_card_clicked(game, board, lenght, size, row=2, col=0)
    on_card_clicked(game, board, lenght, size, row=0, col=3)
    on_card_clicked(game, board, lenght, size, row=2, col=1)
    on_card_clicked(game, board, lenght, size, row=1, col=0)
    on_card_clicked(game, board, lenght, size, row=2, col=2)
    on_card_clicked(game, board, lenght, size, row=1, col=1)
    on_card_clicked(game, board, lenght, size, row=2, col=3)
    assert all_card_showed(game, lenght, size) == True


def test_check_attempts_amount():
    """test sprawdza czy poprawnie nalicza się ilość prób"""
    pair_count = calc_pair_count()
    all_divisors = calc_all_divisors(pair_count)
    unique_divisors = calc_pair_divisors(all_divisors)
    lenght = calc_board_lenght(unique_divisors)
    size = calc_board_size(unique_divisors)
    board = make_test_board()
    game = create_game(board)
    on_card_clicked(game, board, lenght, size, row=0, col=0)
    on_card_clicked(game, board, lenght, size, row=1, col=2)
    assert game['attempts'] == 1
    on_card_clicked(game, board, lenght, size, row=1, col=2)
    assert game['attempts'] == 1
    on_card_clicked(game, board, lenght, size, row=1, col=0)
    assert game['attempts'] == 1
    on_card_clicked(game, board, lenght, size, row=1, col=3)
    assert game['attempts'] == 2


def test_which_card_showed():
    """test sprawdza czy następuje zakrywanie/odkrywanie wybranych kart"""
    pair_count = calc_pair_count()
    all_divisors = calc_all_divisors(pair_count)
    unique_divisors = calc_pair_divisors(all_divisors)
    lenght = calc_board_lenght(unique_divisors)
    size = calc_board_size(unique_divisors)
    board = make_test_board()
    game = create_game(board)
    on_card_clicked(game, board, lenght, size, row=1, col=3)
    on_card_clicked(game, board, lenght, size, row=0, col=3)
    assert board[1][3] == {'value': 1, 'showed': True}
    assert board[0][3] == {'value': 3, 'showed': True}
    on_card_clicked(game, board, lenght, size, row=0, col=0)
    assert board[1][3] == {'value': 1, 'showed': False}
    assert board[0][3] == {'value': 3, 'showed': False}
    assert board[0][0] == {'value': 0, 'showed': True}
    on_card_clicked(game, board, lenght, size, row=1, col=2)
    on_card_clicked(game, board, lenght, size, row=2, col=2)
    assert board[0][0] == {'value': 0, 'showed': True}
    assert board[1][2] == {'value': 0, 'showed': True}
    assert board[2][2] == {'value': 4, 'showed': True}


def get_board_values(board):
    all_values = []
    for row in board:
        for field in row:
            all_values.append(field['value'])
    return all_values


def test_random_board():
    board_1 = run_board_default()
    board_2 = run_board_default()
    assert get_board_values(board_1) != get_board_values(board_2)


def test_time_measure():
    """test sprawdza czy dobrze jest liczony czas od startu do zakończenia gry"""
    pair_count = calc_pair_count()
    all_divisors = calc_all_divisors(pair_count)
    unique_divisors = calc_pair_divisors(all_divisors)
    lenght = calc_board_lenght(unique_divisors)
    size = calc_board_size(unique_divisors)
    board = make_test_board()
    game = create_game(board)
    on_card_clicked(game, board, lenght, size, row=0, col=0)
    time.sleep(2)
    on_card_clicked(game, board, lenght, size, row=1, col=2)
    on_card_clicked(game, board, lenght, size, row=0, col=1)
    on_card_clicked(game, board, lenght, size, row=1, col=3)
    on_card_clicked(game, board, lenght, size, row=0, col=2)
    on_card_clicked(game, board, lenght, size, row=2, col=0)
    on_card_clicked(game, board, lenght, size, row=0, col=3)
    on_card_clicked(game, board, lenght, size, row=2, col=1)
    on_card_clicked(game, board, lenght, size, row=1, col=0)
    on_card_clicked(game, board, lenght, size, row=2, col=2)
    on_card_clicked(game, board, lenght, size, row=1, col=1)
    assert game['finish_at'] == None
    on_card_clicked(game, board, lenght, size, row=2, col=3)
    assert game['started_at'] < game['finish_at']

