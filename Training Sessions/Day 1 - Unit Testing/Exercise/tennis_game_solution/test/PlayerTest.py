import unittest

from Player import Player


class PlayerTest(unittest.TestCase):
    FEDERER = 'Federer'
    NADAL = 'Nadal'

    def test_player_name(self):
        # Arrange
        player = Player(self.FEDERER, 0)
        # Act
        name = player.name
        # Assert
        self.assertEqual(self.FEDERER, name)

    def test_player_score(self):
        # Arrange
        player = Player(self.FEDERER, 2)
        # Act
        score = player.score
        # Assert
        self.assertEqual(2, score)

    def test_increment(self):
        # Arrange
        player = Player(self.FEDERER, 1)
        # Act
        player.increment_score()
        score = player.score
        # Assert
        self.assertEqual(2, score)

    def test_score_zero_as_love(self):
        # Arrange
        player = Player(self.FEDERER, 0)
        # Act
        score = player.get_score_as_string()
        # Assert
        self.assertEqual('love', score)

    def test_score_one_as_fifteen(self):
        # Arrange
        player = Player(self.FEDERER, 1)
        # Act
        score = player.get_score_as_string()
        # Assert
        self.assertEqual('fifteen', score)

    def test_score_two_as_thirty(self):
        # Arrange
        player = Player(self.FEDERER, 2)
        # Act
        score = player.get_score_as_string()
        # Assert
        self.assertEqual('thirty', score)

    def test_score_three_as_forty(self):
        # Arrange
        player = Player(self.FEDERER, 3)
        # Act
        score = player.get_score_as_string()
        # Assert
        self.assertEqual('forty', score)

    def test_invalid_negative_score(self):
        # Arrange
        player = Player(self.FEDERER, -1)
        # Act
        score = player.get_score_as_string()
        # Assert
        self.assertIsNone(score)

    def test_invalid_positive_score(self):
        # Arrange
        player = Player(self.FEDERER, 4)
        # Act
        score = player.get_score_as_string()
        # Assert
        self.assertIsNone(score)

    def test_there_is_tie(self):
        # Arrange
        player1 = Player(self.FEDERER, 2)
        player2 = Player(self.NADAL, 2)
        # Act
        tie = player1.is_tied_with(player2)
        # Assert
        self.assertTrue(tie)

    def test_there_is_not_tie(self):
        # Arrange
        player1 = Player(self.FEDERER, 2)
        player2 = Player(self.NADAL, 3)
        # Act
        tie = player1.is_tied_with(player2)
        # Assert
        self.assertFalse(tie)

    def test_has_at_least_forty_points(self):
        # Arrange
        player = Player(self.FEDERER, 3)
        # Act
        result = player.has_at_least_forty_points()
        # Assert
        self.assertTrue(result)

    def test_has_not_at_least_forty_points(self):
        # Arrange
        player = Player(self.FEDERER, 2)
        # Act
        result = player.has_at_least_forty_points()
        # Assert
        self.assertFalse(result)

    def test_has_less_than_forty_points(self):
        # Arrange
        player = Player(self.FEDERER, 2)
        # Act
        result = player.has_less_than_forty_points()
        # Assert
        self.assertTrue(result)

    def test_has_not_less_than_forty_points(self):
        # Arrange
        player = Player(self.FEDERER, 3)
        # Act
        result = player.has_less_than_forty_points()
        # Assert
        self.assertFalse(result)

    def test_has_more_than_forty_points(self):
        # Arrange
        player = Player(self.FEDERER, 4)
        # Act
        result = player.has_more_than_forty_points()
        # Assert
        self.assertTrue(result)

    def test_has_not_more_than_forty_points(self):
        # Arrange
        player = Player(self.FEDERER, 3)
        # Act
        result = player.has_more_than_forty_points()
        # Assert
        self.assertFalse(result)

    def test_has_one_point_advantage(self):
        # Arrange
        player1 = Player(self.FEDERER, 4)
        player2 = Player(self.NADAL, 3)
        # Act
        result = player1.has_one_point_advantage_on(player2)
        # Assert
        self.assertTrue(result)

    def test_has_not_one_point_advantage(self):
        # Arrange
        player1 = Player(self.FEDERER, 3)
        player2 = Player(self.NADAL, 3)
        # Act
        result = player1.has_one_point_advantage_on(player2)
        # Assert
        self.assertFalse(result)

    def test_has_not_one_point_advantage_with_score_difference_of_two(self):
        # Arrange
        player1 = Player(self.FEDERER, 3)
        player2 = Player(self.NADAL, 5)
        # Act
        result = player1.has_one_point_advantage_on(player2)
        # Assert
        self.assertFalse(result)

    def test_has_at_least_two_points_advantage(self):
        # Arrange
        player1 = Player(self.FEDERER, 5)
        player2 = Player(self.NADAL, 3)
        # Act
        result = player1.has_at_least_two_points_advantage_on(player2)
        # Assert
        self.assertTrue(result)

    def test_has_not_at_least_two_points_advantage(self):
        # Arrange
        player1 = Player(self.FEDERER, 5)
        player2 = Player(self.NADAL, 4)
        # Act
        result = player1.has_at_least_two_points_advantage_on(player2)
        # Assert
        self.assertFalse(result)