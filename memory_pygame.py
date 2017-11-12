import time
import os
import pygame as pg
import memory_engine as engine
import helpers as helper

display_width, display_height = helper.calc_board_size_pixels()
display_size = (display_width, display_height)
card_list = helper.get_cards()
card_size = helper.calc_card_size(card_list)

FPS = 5

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

font_name = pg.font.match_font('arial')
ATTEMPTS = 'attempts: '

GAME_OVER = 0
CONTINUE_GAME = 1

def prepare_resources():
    directory = "resources/images/"
    images_list = []
    keys_list = []
    for file in os.listdir(directory):
        if os.path.splitext(file)[1] == '.jpg' and os.path.splitext(file)[0].startswith("img"):
            keys_list.append(os.path.splitext(file)[0])
            images_list.append(os.path.join(file))
            keys_list.sort()
            images_list.sort()
    return keys_list, images_list


def prepare_dark_resources():
    directory = "resources/dark_images/"
    dark_img_list = []
    dark_keys = []
    for file in os.listdir(directory):
        if os.path.splitext(file)[1] == '.jpg' and os.path.splitext(file)[0].startswith("img"):
            dark_keys.append(os.path.splitext(file)[0])
            dark_img_list.append(os.path.join(file))
            dark_keys.sort()
            dark_img_list.sort()
    return dark_keys, dark_img_list


def load_resources(keys_list, images_list):
    images = {}
    resources = {}
    for key, image in zip(keys_list, images_list):
        images[key] = normalize_image(pg.image.load('resources/images/'+ image))
    resources['images'] = images
    resources['cov_card'] = {'covered_card': normalize_image(pg.image.load('resources/covered_card/img1.jpg'))}
    resources['sound'] = {'song1': pg.mixer.Sound('resources/music/applause.wav')}
    return resources


def load_dark_resources(dark_keys, dark_img_list):
    dark_images = {}
    dark_resources = {}
    for key, image in zip(dark_keys, dark_img_list):
        dark_images[key] = normalize_image(pg.image.load('resources/dark_images/'+ image))
    dark_resources['images'] = dark_images
    return dark_resources


def make_images(resources, keys_list):
    images = []
    for key in keys_list:
        images.append(resources['images'][key])
    return dict(enumerate(images))


def make_dark_images(dark_resources, dark_keys):
    dark_images = []
    for key in dark_keys:
        dark_images.append(dark_resources['images'][key])
    return dict(enumerate(dark_images))


def run_game(resources, dark_resources, images_res, dark_images_res):
    pg.display.set_caption("Memory game")
    game_display = pg.display.set_mode((display_width, display_height))
    all_divisors = helper.calc_all_divisors(card_list)
    unique_divisors = helper.calc_pair_divisors(all_divisors)
    columns = helper.calc_board_columns(unique_divisors)
    rows = helper.calc_board_rows(unique_divisors)
    board = engine.run_board_default()
    clock = pg.time.Clock()
    game = engine.create_game(board)
    draw_attempts = attempts(game)
    draw_text(game_display, ATTEMPTS, 18, 50, 5)
    board_view = make_board_view(board, display_size, images_res, dark_images_res)
    input_data = {'exit': False}

    while not input_data['exit']:
        input_data = process_events(game)
        if GAME_OVER == update_game(game, board, input_data, columns, rows, resources):
            time.sleep(1)
            break
        render_game(board_view, game_display, resources, dark_resources, game, board)
        clock.tick(FPS)

    pg.display.quit()


def draw_text(surface, text, rows, x, y):
    font = pg.font.Font(font_name, rows)
    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)


def process_events(game):

    input_data = {
        'clicked_pos': None,
        'exit': False
    }

    for event in pg.event.get():
        if event.type == pg.QUIT:
            input_data['exit'] = True
        if event.type == pg.MOUSEBUTTONDOWN:
            point = pg.mouse.get_pos()
            card_index = calc_card_index(game['board'], point)
            input_data['exit'] = False
            try:
                input_data['clicked_pos'] = (card_index[0], card_index[1])
            except TypeError:
                continue
    return input_data


def update_game(game, board, input_data, columns, rows, resources):
    if input_data['clicked_pos']:
        row, col = input_data['clicked_pos']
        engine.on_card_clicked(game, board, columns, rows, row, col)
        play_sound(resources, game, board)
    if engine.all_card_showed(game,columns, rows):
        return GAME_OVER
    return CONTINUE_GAME


def attempts(game):
    return game['attempts']


def calc_card_index(board, point):
    x = helper.START_POINT
    y = helper.START_POINT + 20
    for row in board:
        for _ in row:
            card_geometry = [x, y, card_size, card_size]
            if contains_point(card_geometry, point):
                row_index = y // card_size
                col_index = x // card_size
                return row_index, col_index
            elif click_out_of_card(card_geometry, point):
                pass
            x += (card_size + helper.START_POINT)
        y += (card_size + helper.START_POINT)
        x = helper.START_POINT
    return None


def contains_point(geometry, point):
    x, y, w, h = geometry
    return x + w > point[0] > x and y + h > point[1] > y


def click_out_of_card(geometry, point):
    x, y, w, h = geometry
    return x + w <= point[0] <= x and y + h <= point[1] <= y


def render_game(board_view, game_display, resources, dark_resources, game, board):
    render_cards(board_view['card_views'], game_display, resources, dark_resources, game, board)
    pg.display.update()


def render_cards(card_views, game_display, resources, dark_resources, game, board):
    for card_view in card_views:
        render_card(card_view, game_display, resources)
        render_dark_card(card_view, game_display, dark_resources, game, board)


def normalize_image(image):
    return pg.transform.scale(image, (card_size, card_size))


def render_card(card_view, game_display, resources):
    if card_view['card']['showed']:
        image = card_view['image']
        x = card_view['x']
        y = card_view['y']
        game_display.blit(image, (x, y))
    else:
        image = resources['cov_card']['covered_card']
        x = card_view['x']
        y = card_view['y']
        game_display.blit(image, (x, y))
        pass


def render_dark_card(card_view, game_display, dark_resources, game, board):
    if not engine.if_first_round(game) and engine.if_first_turn_in_round(game):
        card_1 = engine.get_active_card_2(game, board)
        card_2 = engine.get_active_card_1(game, board)
        if card_1 != card_2:
            if card_view['card']['value'] == card_1['value'] and card_view['card']['showed']:
                dark_image_1 = card_view['dark_image']
                x = card_view['x']
                y = card_view['y']
                game_display.blit(dark_image_1, (x, y))
            if card_view['card']['value'] == card_2['value'] and card_view['card']['showed']:
                dark_image_2 = card_view['dark_image']
                x = card_view['x']
                y = card_view['y']
                game_display.blit(dark_image_2, (x, y))


def play_sound(resources, game, board):
    if not engine.if_first_round(game) and engine.if_first_turn_in_round(game):
        card_1 = engine.get_active_card_2(game, board)
        card_2 = engine.get_active_card_1(game, board)
        if card_1 == card_2:
            applause = resources['sound']['song1']
            applause.play()


def make_board_view(board, window_rows, images_res, dark_images_res):
    return {
        'board': board,
        'card_views': make_card_views(
            cards=board,
            images=images_res,
            dark_images=dark_images_res)
    }


def make_card_views(cards, images, dark_images):
    x = helper.START_POINT
    y = helper.START_POINT + 20
    card_views = []
    for row in cards:
        for card in row:
            img_1 = images[card['value']]
            img_2 = dark_images[card['value']]
            card_view = make_card_view(x, y, card, img_1, img_2)
            card_views.append(card_view)
            x += (card_size + helper.START_POINT)
        y += (card_size + helper.START_POINT)
        x = helper.START_POINT
    return card_views


def make_card_view(x, y, card, img_1, img_2):
    return {
        'x': x,
        'y': y,
        'card': card,
        'image': img_1,
        'dark_image': img_2
    }


def main():
    pg.init()
    keys_list, images_list = prepare_resources()
    resources = load_resources(keys_list, images_list)
    images_res = make_images(resources, keys_list)
    dark_keys, dark_img_list = prepare_dark_resources()
    dark_resources = load_dark_resources(dark_keys, dark_img_list)
    dark_images_res = make_dark_images(dark_resources, dark_keys)
    run_game(resources, dark_resources, images_res, dark_images_res)
    pg.quit()


main()

