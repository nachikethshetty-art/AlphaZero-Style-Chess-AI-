from multiprocessing import Pool
from self_play import play_game


def run_selfplay_games(num_games=4):

    with Pool(num_games) as pool:

        results = pool.map(play_game, range(num_games))

    data = []

    for game in results:
        data.extend(game)

    return data