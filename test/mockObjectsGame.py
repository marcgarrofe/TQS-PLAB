from src.game import Game
from src.game import Card


# Mock Game 0
draw_pile = [Card('spades', 13), Card('clubs', 1), Card('diamonds', 2),
             Card('hearts', 13, visible=True)]
goal_pile = [[Card('diamonds', 1, visible=True)], [], [], []]
tableau_pile = [[Card('diamonds', 7, visible=True)],
                [Card('spades', 8), Card('spades', 6, visible=True)],
                [Card('diamonds', 11, visible=True), Card('spades', 10, visible=True)],
                [Card('diamonds', 9, visible=True)],
                [Card('spades', 12, visible=True)],
                [Card('clubs', 13, visible=True)],
                []]

test_game_0 = Game(draw_pile=draw_pile, goal_pile=goal_pile, tableau_pile=tableau_pile)

# Mock Game 1
tableau_pile = [[Card('diamonds', 9, visible=False), Card('spades', 8, visible=True),
                 Card('diamonds', 7, visible=True), Card('spades', 6, visible=True)],
                [Card('spades', 10, visible=True)],
                [Card('hearts', 10, visible=True)],
                [Card('hearts', 9, visible=True)],
                [Card('spades', 9, visible=True)],
                [],
                []]

test_game_1 = Game(draw_pile=[Card('spades', 8, visible=True)],
                   goal_pile=[], tableau_pile=tableau_pile)

# Mock Game 2
tableau_pile = [[Card('diamonds', 2, visible=True)],
                [Card('diamonds', 3, visible=True)],
                [Card('spades', 1, visible=True)],
                [Card('hearts', 3, visible=True), Card('hearts', 2, visible=True)],
                [],
                [],
                []]

test_game_2 = Game(draw_pile=[],
                   goal_pile=[[Card('diamonds', 1, visible=True)], [Card('clubs', 1, visible=True)], [], []],
                   tableau_pile=tableau_pile)

# Mock Game 3
tableau_pile = [[],
                [],
                [Card('spades', 1, visible=True)],
                [Card('hearts', 3, visible=True), Card('clubs', 2, visible=True)],
                [],
                [],
                []]
test_game_3 = Game(draw_pile=[],
                   goal_pile=[[Card('diamonds', 1, visible=True)], [Card('clubs', 1, visible=True)], [], []],
                   tableau_pile=tableau_pile)

# Mock Game 4
tableau_pile = [[], [],
                [Card('spades', 1, visible=True)],
                [Card('clubs', 2, visible=True)],
                [], [], []]
test_game_4 = Game(draw_pile=[Card('clubs', 3, visible=True)],
                   goal_pile=[[Card('diamonds', 1, visible=True)], [Card('clubs', 1, visible=True)], [], []],
                   tableau_pile=tableau_pile)

# Mock Game 5
tableau_pile = [[], [], [], [], [], [], []]
goal_pile = [[Card('diamonds', 1, visible=True)], [Card('clubs', 1, visible=True)], [], []]
draw_pile = [Card('diamonds', 2, visible=True)]
test_game_5 = Game(draw_pile=draw_pile, goal_pile=goal_pile, tableau_pile=tableau_pile)

# Mock Game 6
tableau_pile = [[], [], [], [], [], [], []]
goal_pile = [[], [Card('clubs', 2, visible=True)], [], []]
draw_pile = [Card('diamonds', 1, visible=True)]
test_game_6 = Game(draw_pile=draw_pile, goal_pile=goal_pile, tableau_pile=tableau_pile)

# Mock Game 7
tableau_pile = [[], [], [], [], [], [], []]
goal_pile = [[Card('diamonds', 1, visible=True)], [], [], []]
draw_pile = [Card('diamonds', 2), Card('diamonds', 3, visible=True)]
test_game_7 = Game(draw_pile=draw_pile, goal_pile=goal_pile, tableau_pile=tableau_pile)

# Mock Game 8
tableau_pile = [[], [], [], [], [], [], []]
goal_pile = [[Card('diamonds', 1, visible=True)], [], [], []]
draw_pile = [Card('diamonds', 3), Card('diamonds', 2, visible=True)]
test_game_8 = Game(draw_pile=draw_pile, goal_pile=goal_pile, tableau_pile=tableau_pile)


mock_game_list = [test_game_0,
                  test_game_1,
                  test_game_2,
                  test_game_3,
                  test_game_4,
                  test_game_5,
                  test_game_6,
                  test_game_7,
                  test_game_8]
