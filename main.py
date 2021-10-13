import random


def generating_domino():
    all_pieces = []
    for i in range(7):
        for j in range(i, 7):
            all_pieces.append([i, j])
            random.shuffle(all_pieces[len(all_pieces) - 1])
    random.shuffle(all_pieces)
    return all_pieces


def split_between_players(player_pieces, computer_pieces, stock_pieces):
    n = 7
    for i in range(n):
        for role in [player_pieces, computer_pieces]:
            random_pieces_id = random.randint(0, len(stock_pieces) - 1)
            role.append(stock_pieces[random_pieces_id])
            del stock_pieces[random_pieces_id]


def determine_status(player_pieces, computer_pieces, domino_snake):
    # status = 1 - player,status = 2 - computer
    status = 0
    first_player = ""
    # first element of best_double - maximum value on double pieces,second - it's id,
    # -1 - best not found
    best_double = [-1, -1]
    for i in range(7):
        if player_pieces[i][0] == player_pieces[i][1] and computer_pieces[i][0] == computer_pieces[i][1]:
            if player_pieces[i][0] > computer_pieces[i][0] and player_pieces[i][0] > best_double[0]:
                best_double = [player_pieces[i][0], i]
                status = 1
            elif computer_pieces[i][0] > best_double[0]:
                best_double = [computer_pieces[i][0], i]
                status = 2
        elif player_pieces[i][0] == player_pieces[i][1]:
            if player_pieces[i][0] > best_double[0]:
                best_double = [player_pieces[i][0], i]
                status = 1
        elif computer_pieces[i][0] == computer_pieces[i][1]:
            if computer_pieces[i][0] > best_double[0]:
                best_double = [computer_pieces[i][0], i]
                status = 2

    if status == 0:
        is_found = False
    else:
        is_found = True
        if status == 1:
            domino_snake.append(player_pieces[best_double[1]])
            del player_pieces[best_double[1]]
        elif status == 2:
            domino_snake.append(computer_pieces[best_double[1]])
            del computer_pieces[best_double[1]]
    if status == 1:
        first_player = "computer"
    elif status == 2:
        first_player = "player"

    return is_found, first_player


def game_start(stock_pieces, computer_pieces, player_pieces, domino_snake, status):
    first_player_found = False

    while first_player_found is False:
        player_pieces.clear()
        computer_pieces.clear()
        domino_snake.clear()
        stock_pieces.clear()
        stock_pieces = generating_domino()
        split_between_players(player_pieces, computer_pieces, stock_pieces)
        first_player_found, status = determine_status(player_pieces, computer_pieces, domino_snake)

    printing_info(player_pieces, computer_pieces, domino_snake, stock_pieces, status)
    getting_status(status)
    return stock_pieces, status


def printing_info(player_pieces, computer_pieces, domino_snake, stock_pieces, status):
    print("=" * 70)
    print("Stock size:", len(stock_pieces))
    print("Computer pieces:", len(computer_pieces), '\n')
    if len(domino_snake) > 6:
        for i in range(3):
            print(domino_snake[i], end='')
        print('...', end='')
        for i in range(3, 0, -1):
            print(domino_snake[-i], end='')
    else:
        for snake_piece in domino_snake:
            print(snake_piece, end='')

    print('\n')
    print("Your pieces:")
    for i in range(len(player_pieces)):
        print(i+1, ':', player_pieces[i], sep='')
    print('')


def getting_status(status):
    if status == "player":
        print(r"Status: It's your turn to make a move. Enter your command")
    elif status == "computer":
        print(r"Status: Computer is about to make a move. Press Enter to continue...")


def ai_chose(computer_pieces):
    move = random.randint(-len(computer_pieces), len(computer_pieces))
    return move


def strong_ai_computer(computer_pieces, domino_snake):

    snake_and_computer_score = {}

    for i in range(7):
        snake_and_computer_score[i] = 0

    for box in [computer_pieces, domino_snake]:
        for piece in box:
            for i in range(len(piece)):
                snake_and_computer_score[piece[i]] += 1

    computer_pieces_scores = {}

    for index in range(len(computer_pieces)):
        computer_pieces_scores[index] = snake_and_computer_score[computer_pieces[index][0]] + \
                                        snake_and_computer_score[computer_pieces[index][1]]

    sorted_tuple = sorted(computer_pieces_scores.items(), key=lambda x: x[1], reverse=True)

    move = 0
    for elem in sorted_tuple:
        piece = computer_pieces[elem[0]]
        if domino_snake[0][0] == piece[0] or domino_snake[0][0] == piece[1]:
            move = -(1 + elem[0])
            if domino_snake[0][0] == piece[0]:
                piece[0], piece[1] = piece[1], piece[0]
            break
        elif domino_snake[-1][1] == piece[0] or domino_snake[-1][1] == piece[1]:
            move = (1 + elem[0])
            if domino_snake[-1][1] == piece[1]:
                piece[0], piece[1] = piece[1], piece[0]
            break
        else:
            continue

    return move


def weak_ai_computer(computer_pieces, stock_pieces, domino_snake):
    fl = True
    move = ai_chose(computer_pieces)
    while fl:
        if move < 0:
            if domino_snake[0][0] != computer_pieces[abs(move) - 1][0] and \
               domino_snake[0][0] != computer_pieces[abs(move) - 1][1]:
                move = ai_chose(computer_pieces)
                continue

            if domino_snake[0][0] != computer_pieces[abs(move) - 1][1]:
                computer_pieces[abs(move) - 1][1], computer_pieces[abs(move) - 1][0] =\
                    computer_pieces[abs(move) - 1][0], computer_pieces[abs(move) - 1][1]

        elif move > 0:
            if domino_snake[-1][1] != computer_pieces[abs(move) - 1][0] and \
               domino_snake[-1][1] != computer_pieces[abs(move) - 1][1]:
                move = ai_chose(computer_pieces)
                continue

            if domino_snake[-1][1] != computer_pieces[abs(move) - 1][0]:
                computer_pieces[abs(move) - 1][1], computer_pieces[abs(move) - 1][0] =\
                    computer_pieces[abs(move) - 1][0], computer_pieces[abs(move) - 1][1]

        fl = False
    return move


def taking_turn(stock_pieces, computer_pieces, player_pieces, domino_snake, status, move):

    current_player = []

    if status == "computer":
        move = strong_ai_computer(computer_pieces, domino_snake)
        current_player = computer_pieces
        status = "player"
    elif status == "player":
        current_player = player_pieces
        status = "computer"

    if move < 0:
        domino_snake.insert(0, current_player[abs(move) - 1])
        del current_player[abs(move) - 1]
    elif move > 0:
        domino_snake.append(current_player[move - 1])
        del current_player[move - 1]
    else:
        if len(stock_pieces) != 0:
            current_player.append(stock_pieces[0])
            del stock_pieces[0]
    return status


def is_game_end(stock_pieces, computer_pieces, player_pieces, domino_snake, status):

    if len(computer_pieces) == 0:
        status = "computer"
        print("Status: The game is over. The computer won!")
        return True
    elif len(player_pieces) == 0:
        status = "player"
        print("Status: The game is over. You won!")
        return True
    else:
        if domino_snake[0][0] == domino_snake[-1][1]:
            repeat = 0
            for elem in domino_snake:
                repeat += elem.count(domino_snake[0][0])
            if repeat >= 8:
                status = ''
                print("Status: The game is over. It's a draw!")
                return True

    return False


# input number from console
def entering_number():
    enter = input()
    while True:
        try:
            int(enter)
            break
        except ValueError:
            print("Invalid input. Please try again. \n", end='')
            enter = input()

    move = int(enter)
    return move


# checking is move is valid:
# if not - try again
def getting_move(status, player_pieces, domino_snake):
    fl = True
    if status == "player":
        move = entering_number()
        # in this loop we check if the input of player is correct or legal.
        while fl:
            if abs(move) > len(player_pieces):
                print("Invalid input. Please try again. \n", end='')
                move = entering_number()
                continue

            if move < 0:
                if domino_snake[0][0] != player_pieces[abs(move) - 1][0] and \
                        domino_snake[0][0] != player_pieces[abs(move) - 1][1]:
                    print("Illegal move. Please try again.")
                    move = entering_number()
                    continue

                if domino_snake[0][0] != player_pieces[abs(move) - 1][1]:
                    player_pieces[abs(move) - 1][1], player_pieces[abs(move) - 1][0] = \
                        player_pieces[abs(move) - 1][0], player_pieces[abs(move) - 1][1]

            elif move > 0:
                if domino_snake[-1][1] != player_pieces[abs(move) - 1][0] and \
                        domino_snake[-1][1] != player_pieces[abs(move) - 1][1]:
                    print("Illegal move. Please try again.")
                    move = entering_number()
                    continue

                if domino_snake[-1][1] != player_pieces[abs(move) - 1][0]:
                    player_pieces[abs(move) - 1][1], player_pieces[abs(move) - 1][0] = \
                        player_pieces[abs(move) - 1][0], player_pieces[abs(move) - 1][1]

            if abs(move) > len(player_pieces):
                print("Invalid input. Please try again. \n", end='')
                move = entering_number()
                continue

            fl = False

    else:
        move = input()
    return move


def main():
    player_pieces = []
    computer_pieces = []
    stock_pieces = []
    domino_snake = []
    game_end = False
    status = ""
    stock_pieces, status = game_start(stock_pieces, computer_pieces, player_pieces, domino_snake, status)

    while game_end is False:
        move = getting_move(status, player_pieces, domino_snake)
        status = taking_turn(stock_pieces, computer_pieces, player_pieces, domino_snake, status, move)
        printing_info(player_pieces, computer_pieces, domino_snake, stock_pieces, status)
        game_end = is_game_end(stock_pieces, computer_pieces, player_pieces, domino_snake, status)
        if game_end is not True:
            getting_status(status)


if __name__ == '__main__':
    main()
