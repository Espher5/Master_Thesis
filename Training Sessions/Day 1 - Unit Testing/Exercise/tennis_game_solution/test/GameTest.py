import unittest

from PlayerTest import PlayerTest
from Game import Game
from DuplicatedPlayerError import DuplicatedPlayerError
from GameHasAlreadyBeenWonError import GameHasAlreadyBeenWonError


class GameTest(unittest.TestCase):
    def test_game_player1(self):
        game = Game(PlayerTest.FEDERER, PlayerTest.NADAL)
        name1 = game.get_player1_name()
        self.assertEqual(PlayerTest.FEDERER, name1)

    def test_game_player2(self):
        game = Game(PlayerTest.FEDERER, PlayerTest.NADAL)
        name2 = game.get_player2_name()
        self.assertEqual(PlayerTest.NADAL, name2)

    def test_game_with_duplicated_players(self):
        self.assertRaises(DuplicatedPlayerError, Game, PlayerTest.FEDERER, PlayerTest.FEDERER)

    def test_game_at_beginning(self):
        game = Game(PlayerTest.FEDERER, PlayerTest.NADAL)
        status = game.game_status
        self.assertEqual('Federer love - Nadal love', status)

    def test_first_player_winner(self):
        game = Game(PlayerTest.FEDERER, PlayerTest.NADAL)
        player1 = game.get_player1_name()
        game.increment_player_score(player1)
        game.increment_player_score(player1)
        game.increment_player_score(player1)
        game.increment_player_score(player1)
        status = game.game_status
        self.assertEqual('Federer wins', status)

    def test_second_player_winner(self):
        game = Game(PlayerTest.FEDERER, PlayerTest.NADAL)
        player2 = game.get_player2_name()
        game.increment_player_score(player2)
        game.increment_player_score(player2)
        game.increment_player_score(player2)
        game.increment_player_score(player2)
        status = game.game_status
        self.assertEqual('Nadal wins', status)

    def test_player1_fifteen_player2_love(self):
        game = Game(PlayerTest.FEDERER, PlayerTest.NADAL)
        player1 = game.get_player1_name()
        game.increment_player_score(player1)
        status = game.game_status
        self.assertEqual('Federer fifteen - Nadal love', status)

    def test_deuce(self):
        game = Game(PlayerTest.FEDERER, PlayerTest.NADAL)
        player1 = game.get_player1_name()
        player2 = game.get_player2_name()
        game.increment_player_score(player1)
        game.increment_player_score(player1)
        game.increment_player_score(player1)

        game.increment_player_score(player2)
        game.increment_player_score(player2)
        game.increment_player_score(player2)

        status = game.game_status
        self.assertEqual('Deuce', status)

    def test_advantage_player1(self):
        game = Game(PlayerTest.FEDERER, PlayerTest.NADAL)
        player1 = game.get_player1_name()
        player2 = game.get_player2_name()
        game.increment_player_score(player1)
        game.increment_player_score(player1)
        game.increment_player_score(player1)

        game.increment_player_score(player2)
        game.increment_player_score(player2)
        game.increment_player_score(player2)

        game.increment_player_score(player1)
        status = game.game_status
        self.assertEqual('Advantage Federer', status)

    def test_advantage_player2(self):
        game = Game(PlayerTest.FEDERER, PlayerTest.NADAL)
        player1 = game.get_player1_name()
        player2 = game.get_player2_name()
        game.increment_player_score(player1)
        game.increment_player_score(player1)
        game.increment_player_score(player1)

        game.increment_player_score(player2)
        game.increment_player_score(player2)
        game.increment_player_score(player2)

        game.increment_player_score(player2)
        status = game.game_status
        self.assertEqual('Advantage Nadal', status)

    def test_already_winner(self):
        game = Game(PlayerTest.FEDERER, PlayerTest.NADAL)
        player1 = game.get_player1_name()
        game.increment_player_score(player1)
        game.increment_player_score(player1)
        game.increment_player_score(player1)
        game.increment_player_score(player1)

        self.assertRaises(GameHasAlreadyBeenWonError, game.increment_player_score, player1)
