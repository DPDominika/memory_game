import unittest
import time
from memory_engine import (
    run_board_default, create_game, on_card_clicked,
    count_showed_cards, all_card_showed, create_cards,
    make_game_board, cards_indexes, make_empty_board
)
from helpers import(
    get_cards, calc_all_divisors, calc_pair_divisors,
    calc_board_columns, calc_board_rows, calc_board_size_pixels
)


def make_test_board():
    card_list = get_cards()
    cards = create_cards()
    all_divisors = calc_all_divisors(card_list)
    unique_divisors = calc_pair_divisors(all_divisors)
    columns = calc_board_columns(unique_divisors)
    rows = calc_board_rows(unique_divisors)
    indexes = cards_indexes(columns)
    board = make_empty_board(rows, columns)
    make_game_board(board, indexes, cards)
    return board


def get_board_values(board):
    all_values = []
    for row in board:
        for field in row:
            all_values.append(field['value'])
    return all_values


class TestMemory(unittest.TestCase):

    def test_calc_board_rows(self):
        card_list = get_cards()
        all_divisors = calc_all_divisors(card_list)
        unique_divisors = calc_pair_divisors(all_divisors)
        self.assertEqual(calc_board_columns(unique_divisors) * calc_board_rows(unique_divisors), len(card_list) * 2)

    def test_click_good_pair(self):
        card_list = get_cards()
        all_divisors = calc_all_divisors(card_list)
        unique_divisors = calc_pair_divisors(all_divisors)
        columns = calc_board_columns(unique_divisors)
        rows = calc_board_rows(unique_divisors)
        board = make_test_board()
        game = create_game(board)
        on_card_clicked(game, board, columns, rows, row=1, col=1)
        self.assertEqual(count_showed_cards(game), 1)
        on_card_clicked(game, board, columns, rows, row=2, col=3)
        self.assertEqual(count_showed_cards(game), 2)
        on_card_clicked(game, board, columns, rows, row=0, col=0)
        self.assertEqual(count_showed_cards(game), 3)
        on_card_clicked(game, board, columns, rows, row=1, col=2)
        self.assertEqual(count_showed_cards(game), 4)

    def test_click_same_pair(self):
        card_list = get_cards()
        all_divisors = calc_all_divisors(card_list)
        unique_divisors = calc_pair_divisors(all_divisors)
        columns = calc_board_columns(unique_divisors)
        rows = calc_board_rows(unique_divisors)
        board = make_test_board()
        game = create_game(board)
        on_card_clicked(game, board, columns, rows, row=1, col=1)
        self.assertEqual(count_showed_cards(game), 1)
        on_card_clicked(game, board, columns, rows, row=1, col=1)
        self.assertEqual(count_showed_cards(game), 1)

    def test_if_game_is_finished(self):
        card_list = get_cards()
        all_divisors = calc_all_divisors(card_list)
        unique_divisors = calc_pair_divisors(all_divisors)
        columns = calc_board_columns(unique_divisors)
        rows = calc_board_rows(unique_divisors)
        board = make_test_board()
        game = create_game(board)
        on_card_clicked(game, board, columns, rows, row=0, col=0)
        on_card_clicked(game, board, columns, rows, row=1, col=2)
        on_card_clicked(game, board, columns, rows, row=0, col=1)
        on_card_clicked(game, board, columns, rows, row=1, col=3)
        on_card_clicked(game, board, columns, rows, row=0, col=2)
        on_card_clicked(game, board, columns, rows, row=2, col=0)
        on_card_clicked(game, board, columns, rows, row=0, col=3)
        on_card_clicked(game, board, columns, rows, row=2, col=1)
        on_card_clicked(game, board, columns, rows, row=1, col=0)
        on_card_clicked(game, board, columns, rows, row=2, col=2)
        on_card_clicked(game, board, columns, rows, row=1, col=1)
        on_card_clicked(game, board, columns, rows, row=2, col=3)
        self.assertTrue(all_card_showed(game, columns, rows), True)

    def test_check_attempts_amount(self):
        card_list = get_cards()
        all_divisors = calc_all_divisors(card_list)
        unique_divisors = calc_pair_divisors(all_divisors)
        columns = calc_board_columns(unique_divisors)
        rows = calc_board_rows(unique_divisors)
        board = make_test_board()
        game = create_game(board)
        on_card_clicked(game, board, columns, rows, row=0, col=0)
        on_card_clicked(game, board, columns, rows, row=1, col=2)
        self.assertEqual(game['attempts'], 1)
        on_card_clicked(game, board, columns, rows, row=1, col=2)
        self.assertEqual(game['attempts'], 1)
        on_card_clicked(game, board, columns, rows, row=1, col=0)
        self.assertEqual(game['attempts'], 1)
        on_card_clicked(game, board, columns, rows, row=1, col=3)
        self.assertEqual(game['attempts'], 2)

    def test_which_card_showed(self):
        card_list = get_cards()
        all_divisors = calc_all_divisors(card_list)
        unique_divisors = calc_pair_divisors(all_divisors)
        columns = calc_board_columns(unique_divisors)
        rows = calc_board_rows(unique_divisors)
        board = make_test_board()
        game = create_game(board)
        on_card_clicked(game, board, columns, rows, row=1, col=3)
        on_card_clicked(game, board, columns, rows, row=0, col=3)
        self.assertEqual(board[1][3], {'value': 1, 'showed': True})
        self.assertEqual(board[0][3], {'value': 3, 'showed': True})
        on_card_clicked(game, board, columns, rows, row=0, col=0)
        self.assertEqual(board[1][3], {'value': 1, 'showed': False})
        self.assertEqual(board[0][3], {'value': 3, 'showed': False})
        self.assertEqual(board[0][0], {'value': 0, 'showed': True})
        on_card_clicked(game, board, columns, rows, row=1, col=2)
        on_card_clicked(game, board, columns, rows, row=2, col=2)
        self.assertEqual(board[0][0], {'value': 0, 'showed': True})
        self.assertEqual(board[1][2], {'value': 0, 'showed': True})
        self.assertEqual(board[2][2], {'value': 4, 'showed': True})

    def test_random_board(self):
        board_1 = run_board_default()
        board_2 = run_board_default()
        self.assertNotEqual(get_board_values(board_1) != get_board_values(board_2), False)

    def test_time_measure(self):
        card_list = get_cards()
        all_divisors = calc_all_divisors(card_list)
        unique_divisors = calc_pair_divisors(all_divisors)
        columns = calc_board_columns(unique_divisors)
        rows = calc_board_rows(unique_divisors)
        board = make_test_board()
        game = create_game(board)
        on_card_clicked(game, board, columns, rows, row=0, col=0)
        time.sleep(2)
        on_card_clicked(game, board, columns, rows, row=1, col=2)
        on_card_clicked(game, board, columns, rows, row=0, col=1)
        on_card_clicked(game, board, columns, rows, row=1, col=3)
        on_card_clicked(game, board, columns, rows, row=0, col=2)
        on_card_clicked(game, board, columns, rows, row=2, col=0)
        on_card_clicked(game, board, columns, rows, row=0, col=3)
        on_card_clicked(game, board, columns, rows, row=2, col=1)
        on_card_clicked(game, board, columns, rows, row=1, col=0)
        on_card_clicked(game, board, columns, rows, row=2, col=2)
        on_card_clicked(game, board, columns, rows, row=1, col=1)
        self.assertEqual(game['finish_at'], None)
        on_card_clicked(game, board, columns, rows, row=2, col=3)
        self.assertTrue(game['started_at'] < game['finish_at'], True)


if __name__ == '__main__':
    unittest.main()


