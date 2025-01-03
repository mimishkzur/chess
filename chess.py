# создаем класс всех фигур
class ChessMan(object):
    img = None

    def __init__(self, color):
        self.color = color

    def __repr__(self):
        return self.img[0 if self.color == Color.white else 1]

# класс для определения цвета фигуры
class Color(object):
    dot = 0
    black = 1
    white = 2

# класс точка - точка на игровом поле
class Dot(object):
    color = Color.dot

    def get_moves(self, board, start_x, start_y):
        raise Exception('тут нет фигуры')

    def __repr__(self):
        return '.'

# класс с ходом
class Move:
    def __init__(self, start_x, start_y, end_x, end_y, piece):
        self.start_x = start_x
        self.start_y = start_y
        self.end_x = end_x
        self.end_y = end_y
        self.piece = piece

# класс пешка
class Pawn(ChessMan):
    img = ('P', 'p')

    # получаем возможные ходы
    def get_moves(self, board, start_x, start_y):
        moves = []

        if self.color == Color.white:
            if start_x == 6 and board.get_color(start_x - 1, start_y) == Color.dot and board.get_color(start_x - 2, start_y) == Color.dot:
                moves.append([chr(ord('a') + start_y), 8 - (start_x - 2)])
                moves.append([chr(ord('a') + start_y), 8 - (start_x - 1)])
            elif start_x > 1 and board.get_color(start_x - 1, start_y) == Color.dot:
                moves.append([chr(ord('a') + start_y), 8 - (start_x - 1)])

        elif self.color == Color.black:
            if start_x == 1 and board.get_color(start_x + 1, start_y) == Color.dot and board.get_color(start_x + 2, start_y) == Color.dot:
                moves.append([chr(ord('a') + start_y), 8 - (start_x + 2)])
                moves.append([chr(ord('a') + start_y), 8 - (start_x + 1)])
            elif start_x < 6 and board.get_color(start_x + 1, start_y) == Color.dot:
                moves.append([chr(ord('a') + start_y), 8 - (start_x + 1)])

        return moves

# класс конь
class Knight(ChessMan):
    img = ('N', 'n')

    # получаем возможные ходы
    def get_moves(self, board, start_x, start_y):
        moves = []

        knight_moves = [
            (start_x + 2, start_y + 1),
            (start_x + 1, start_y + 2),
            (start_x - 1, start_y + 2),
            (start_x - 2, start_y + 1),
            (start_x - 2, start_y - 1),
            (start_x - 1, start_y - 2),
            (start_x + 1, start_y - 2),
            (start_x + 2, start_y - 1),
        ]

        for move in knight_moves:
            x, y = move
            if 0 <= x < 8 and 0 <= y < 8 and board.get_color(x, y) != self.color:
                moves.append([chr(ord('a') + y), 8 - x])

        return moves

# класс слон
class Bishop(ChessMan):
    img = ('B', 'b')

    # получаем возможные ходы
    def get_moves(self, board, start_x, start_y):
        moves = []

        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for direction in directions:
            dx, dy = direction
            x, y = start_x + dx, start_y + dy

            while 0 <= x < 8 and 0 <= y < 8:
                if board.get_color(x, y) == self.color:
                    break
                moves.append([chr(ord('a') + y), 8 - x])

                if board.get_color(x, y) != Color.dot:
                    break

                x += dx
                y += dy

        return moves

# класс ладья
class Rook(ChessMan):
    img = ('R', 'r')

    # получаем возможные ходы
    def get_moves(self, board, start_x, start_y):
        moves = []

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

        for direction in directions:
            dx, dy = direction
            x, y = start_x + dx, start_y + dy

            while 0 <= x < 8 and 0 <= y < 8:
                if board.get_color(x, y) == self.color:
                    break
                moves.append([chr(ord('a') + y), 8 - x])

                if board.get_color(x, y) != Color.dot:
                    break

                x += dx
                y += dy

        return moves

# класс королева
class Queen(ChessMan):
    img = ('Q', 'q')

    # получаем возможные ходы
    def get_moves(self, board, start_x, start_y):
        bishop_moves = Bishop(self.color).get_moves(board, start_x, start_y)
        rook_moves = Rook(self.color).get_moves(board, start_x, start_y)

        return bishop_moves + rook_moves

# класс король
class King(ChessMan):
    img = ('K', 'k')

    # получаем возможные ходы
    def get_moves(self, board, start_x, start_y):
        moves = []

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

        for direction in directions:
            dx, dy = direction
            x, y = start_x + dx, start_y + dy

            if 0 <= x < 8 and 0 <= y < 8 and board.get_color(x, y) != self.color:
                moves.append([chr(ord('a') + y), 8 - x])

        return moves

# дополнительные фигуры

# камень (просто может двигаться как ладья и конь)
class Stone(ChessMan):
    img = ('T', 't')

    def get_moves(self, board, start_x, start_y):
        rook_moves = Rook(self.color).get_moves(board, start_x, start_y)
        knight_moves = Knight(self.color).get_moves(board, start_x, start_y)

        return rook_moves + knight_moves

# стрелок (двигается по диагонали, не прыгает через фигуры, стреляет на два шага вперед (по вертикали или горизонтали)
class Archer(ChessMan):
    img = ('A', 'a')

    def get_moves(self, board, start_x, start_y):
        moves = []

        # Движение по диагонали
        directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

        for direction in directions:
            dx, dy = direction
            x, y = start_x + dx, start_y + dy

            while 0 <= x < 8 and 0 <= y < 8:
                if board.get_color(x, y) == self.color:
                    break
                moves.append([chr(ord('a') + y), 8 - x])

                if board.get_color(x, y) != Color.dot:
                    break

                x += dx
                y += dy

        # Стрельба
        straight_shots = [
            (start_x - 2, start_y),
            (start_x + 2, start_y),
            (start_x, start_y - 2),
            (start_x, start_y + 2),
        ]

        for move in straight_shots:
            x, y = move
            if 0 <= x < 8 and 0 <= y < 8 and board.get_color(x, y) != self.color and board.get_color(x, y) != Color.dot:
                moves.append([chr(ord('a') + y), 8 - x])

        return moves

# волшебник (двигается как конь, с фигурой своего цвета может меняться местами (фигура должна находиться рядом))
class Wizard(ChessMan):
    img = ('W', 'w')

    def get_moves(self, board, start_x, start_y):
        moves = []

        knight_moves = [
            (start_x + 2, start_y + 1),
            (start_x + 1, start_y + 2),
            (start_x - 1, start_y + 2),
            (start_x - 2, start_y + 1),
            (start_x - 2, start_y - 1),
            (start_x - 1, start_y - 2),
            (start_x + 1, start_y - 2),
            (start_x + 2, start_y - 1),
        ]

        for move in knight_moves:
            x, y = move
            if 0 <= x < 8 and 0 <= y < 8 and board.get_color(x, y) != self.color:
                moves.append([chr(ord('a') + y), 8 - x])

        # добавляем возможные ходы для обмена местами
        friendly_moves = [
            (start_x + 1, start_y),
            (start_x - 1, start_y),
            (start_x, start_y + 1),
            (start_x, start_y - 1),
        ]

        for move in friendly_moves:
            x, y = move
            if 0 <= x < 8 and 0 <= y < 8 and board.get_color(x, y) == self.color:
                moves.append([chr(ord('a') + y), 8 - x])

        return moves


# класс шашка
class CheckersPiece(ChessMan):
    img = ('C', 'c')

    def get_moves(self, board, start_x, start_y):
        moves = []

        # ходы для белых шашек
        if self.color == Color.white:
            # движение вперед-влево
            if start_x > 0 and start_y > 0 and board.get_color(start_x - 1, start_y - 1) == Color.dot:
                moves.append([chr(ord('a') + start_y - 1), 8 - (start_x - 1)])
            # движение вперед-вправо
            if start_x > 0 and start_y < 7 and board.get_color(start_x - 1, start_y + 1) == Color.dot:
                moves.append([chr(ord('a') + start_y + 1), 8 - (start_x - 1)])
            # возможность съесть фигуру вперед-влево
            if start_x > 1 and start_y > 1 and board.get_color(start_x - 1, start_y - 1) == Color.black and \
                    board.get_color(start_x - 2, start_y - 2) == Color.dot:
                moves.append([chr(ord('a') + start_y - 2), 8 - (start_x - 2)])
            # возможность съесть фигуру вперед-вправо
            if start_x > 1 and start_y < 6 and board.get_color(start_x - 1, start_y + 1) == Color.black and \
                    board.get_color(start_x - 2, start_y + 2) == Color.dot:
                moves.append([chr(ord('a') + start_y + 2), 8 - (start_x - 2)])

        # ходы для черных шашек
        elif self.color == Color.black:
            # движение назад-влево
            if start_x < 7 and start_y > 0 and board.get_color(start_x + 1, start_y - 1) == Color.dot:
                moves.append([chr(ord('a') + start_y - 1), 8 - (start_x + 1)])
            # движение назад-вправо
            if start_x < 7 and start_y < 7 and board.get_color(start_x + 1, start_y + 1) == Color.dot:
                moves.append([chr(ord('a') + start_y + 1), 8 - (start_x + 1)])
            # возможность съесть фигуру назад-влево
            if start_x < 6 and start_y > 1 and board.get_color(start_x + 1, start_y - 1) == Color.white and \
                    board.get_color(start_x + 2, start_y - 2) == Color.dot:
                moves.append([chr(ord('a') + start_y - 2), 8 - (start_x + 2)])
            # возможность съесть фигуру назад-вправо
            if start_x < 6 and start_y < 6 and board.get_color(start_x + 1, start_y + 1) == Color.white and \
                    board.get_color(start_x + 2, start_y + 2) == Color.dot:
                moves.append([chr(ord('a') + start_y + 2), 8 - (start_x + 2)])

        return moves

class Board(object):
    def __init__(self):
        self.board = [[Dot()] * 8 for _ in range(8)]
        self.move_list = []
        self.select_chess_set()

    # выбираем тип игры
    def select_chess_set(self):
        print('выберите тип шахмат:')
        print('1. обычные шахматы')
        print('2. шахматы с новыми фигурами')
        print('3. шашки')

        choice = input('введите номер выбранного типа шахмат: ')

        if choice == '1':
            self.set_up_classic_chess()
            self.play_chess_game()
        elif choice == '2':
            self.set_up_custom_chess()
            self.play_chess_game()
        elif choice == '3':
            self.set_up_checkers()
            self.play_checkers_game()
        else:
            print('неверный выбор. используются обычные шахматы.')
            self.set_up_classic_chess()

    def set_up_classic_chess(self):
        for i in range(8):
            self.board[1][i] = Pawn(Color.black)
            self.board[6][i] = Pawn(Color.white)

        self.board[0][0], self.board[0][7] = Rook(Color.black), Rook(Color.black)
        self.board[7][0], self.board[7][7] = Rook(Color.white), Rook(Color.white)

        self.board[0][1], self.board[0][6] = Knight(Color.black), Knight(Color.black)
        self.board[7][1], self.board[7][6] = Knight(Color.white), Knight(Color.white)

        self.board[0][2], self.board[0][5] = Bishop(Color.black), Bishop(Color.black)
        self.board[7][2], self.board[7][5] = Bishop(Color.white), Bishop(Color.white)

        self.board[0][3], self.board[7][3] = Queen(Color.black), Queen(Color.white)
        self.board[0][4], self.board[7][4] = King(Color.black), King(Color.white)

    def set_up_custom_chess(self):
        for i in range(8):
            self.board[1][i] = Pawn(Color.black)
            self.board[6][i] = Pawn(Color.white)

        self.board[0][0], self.board[0][7] = Stone(Color.black), Stone(Color.black)
        self.board[7][0], self.board[7][7] = Stone(Color.white), Stone(Color.white)

        self.board[0][1], self.board[0][6] = Archer(Color.black), Archer(Color.black)
        self.board[7][1], self.board[7][6] = Archer(Color.white), Archer(Color.white)

        self.board[0][2], self.board[0][5] = Wizard(Color.black), Wizard(Color.black)
        self.board[7][2], self.board[7][5] = Wizard(Color.white), Wizard(Color.white)

        self.board[0][3], self.board[7][3] = Queen(Color.black), Queen(Color.white)
        self.board[0][4], self.board[7][4] = King(Color.black), King(Color.white)

    def set_up_checkers(self):
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 1:
                    if i < 3:
                        self.board[i][j] = CheckersPiece(Color.black)
                    elif i > 4:
                        self.board[i][j] = CheckersPiece(Color.white)

    # получаем цвет фигуры
    def get_color(self, start_x, start_y):
        return self.board[start_x][start_y].color

    # проверка на условие "король жив"
    def is_king_alive(self, color):
        for row in self.board:
            for piece in row:
                if isinstance(piece, King) and piece.color == color:
                    return True
        return False

    # получаем все возможные ходы
    def get_moves(self, start_x, start_y):
        return self.board[start_x][start_y].get_moves(self, start_x, start_y)

    # добавляем ход в список ходов
    def push_move(self, start_x, start_y, end_x, end_y, piece):
        move = Move(start_x, start_y, end_x, end_y, piece)
        self.move_list.append(move)

    # убираем ход из списка ходов
    def pop_moves(self, count=1):

        for _ in range(count):
            if self.move_list:
                move = self.move_list.pop()
                self.board[move.start_x][move.start_y] = move.piece
                self.board[move.end_x][move.end_y] = Dot()
            else:
                print('больше ходов отменить нельзя. достигнуто начальное состояние.')
                break

    # получаем координаты фигуры от пользователя
    def input_piece(self):
        piece = input("введите координаты фигуры, которой хотите походить (например, 'e2'): ")
        try:
            start_x, start_y = 8 - int(piece[1]), ord(piece[0]) - ord('a')
            return start_x, start_y
        except ValueError or IndexError:
            print('неправильный формат ввода. попробуйте еще раз.')
            return self.input_piece()

    # получаем координаты от пользователя, на которые надо сходить
    def input_move(self):
        move = input("введите координаты, на которые хотите сходить (например, 'e2'): ")
        try:
            end_y, end_x = ord(move[0]) - ord('a'), 8 - int(move[1])
            return end_x, end_y
        except (ValueError, IndexError):
            print('неправильный формат ввода. попробуйте еще раз')
            return self.input_move()

    # вывод доски для игры
    def display_board(self):
        res = ''
        for i in range(8):
            res += f"{8 - i} {' '.join(map(str, self.board[i]))} {8 - i}"
            res += '\n'
        return print(f'  a b c d e f g h\n{res}  a b c d e f g h')

    # проверка на наличие фишек для шашек
    def are_pieces_left(self, color):
        for row in self.board:
            for piece in row:
                if piece.color == color:
                    return True
        return False

    # сама игра
    def play_chess_game(self):
        c = 0
        while self.is_king_alive(Color.white) and self.is_king_alive(Color.black):
            self.display_board()
            print('ход белых' if c % 2 == 0 else 'ход черных')
            start_x, start_y = self.input_piece()
            valid_moves = self.get_moves(start_x, start_y)

            # временная копия доски
            temp_board = [row[:] for row in self.board]

            # подсвечиваем доступные ходы
            for i in range(8):
                for j in range(8):
                    if [chr(ord('a') + j), 8 - i] in valid_moves:
                        temp_board[i][j] = '\033[42m' + str(self.board[i][j]) + '\033[0m'

            # выводим доску с доступными ходами
            print('доступные ходы: ')
            print('  a b c d e f g h')
            for i, row in enumerate(temp_board, start=1):
                print(f"{9 - i} {' '.join(map(str, row))} {9 - i}")
            print('  a b c d e f g h')

            end_x, end_y = self.input_move()
            temp_x, temp_y = chr(ord('a') + end_y), 8 - end_x # координаты в шахматном виде

            if [temp_x, temp_y] in valid_moves:
                piece = self.board[start_x][start_y]
                if isinstance(piece, Wizard):
                    self.push_move(start_x, start_y, end_x, end_y, piece)
                    self.board[end_x][end_y], self.board[start_x][start_y] = self.board[start_x][start_y], self.board[end_x][end_y]
                    c += 1
                elif isinstance(piece, Archer):
                    self.push_move(start_x, start_y, end_x, end_y, piece)
                    if isinstance(self.board[end_x][end_y], Dot):
                        self.board[end_x][end_y], self.board[start_x][start_y] = self.board[start_x][start_y], self.board[end_x][end_y]
                    else:
                        self.board[end_x][end_y], self.board[start_x][start_y] = Dot(), self.board[start_x][start_y]
                else:
                    self.push_move(start_x, start_y, end_x, end_y, piece)

                    self.board[end_x][end_y] = self.board[start_x][start_y]
                    self.board[start_x][start_y] = Dot()
                    c += 1
            else:
                print('неправильный ход. попробуйте еще раз.')
                continue

            undo = input('хотите отменить последний ход или возвратиться на несколько ходов? (y/n/число): ')

            if undo.lower() == 'y':
                self.pop_moves()
                c -= 1
            elif undo.isdigit():
                count = int(undo)
                self.pop_moves(count)
                c -= count

        print('игра окончена. победили ', 'белые' if self.is_king_alive(Color.white) else 'черные')

    def play_checkers_game(self):
        c = 0
        while self.are_pieces_left(Color.white) and self.are_pieces_left(Color.black):
            self.display_board()
            print('ход белых' if c % 2 == 0 else 'ход черных')
            start_x, start_y = self.input_piece()
            valid_moves = self.get_moves(start_x, start_y)

            # временная копия доски
            temp_board = [row[:] for row in self.board]

            # подсвечиваем доступные ходы
            for i in range(8):
                for j in range(8):
                    if [chr(ord('a') + j), 8 - i] in valid_moves:
                        temp_board[i][j] = '\033[42m' + str(self.board[i][j]) + '\033[0m'

            print('доступные ходы: ')
            print('  a b c d e f g h')
            for i, row in enumerate(temp_board, start=1):
                print(f"{9 - i} {' '.join(map(str, row))} {9 - i}")
            print('  a b c d e f g h')

            end_x, end_y = self.input_move()
            temp_x, temp_y = chr(ord('a') + end_y), 8 - end_x  # координаты в шашечном виде

            if [temp_x, temp_y] in valid_moves:
                piece = self.board[start_x][start_y]
                # удаляем шашку, через которую перепрыгнули
                jump_x, jump_y = (start_x + end_x) // 2, (start_y + end_y) // 2
                self.board[jump_x][jump_y] = Dot()

                self.push_move(start_x, start_y, end_x, end_y, piece)

                self.board[end_x][end_y] = self.board[start_x][start_y]
                self.board[start_x][start_y] = Dot()
                c += 1
            else:
                print('неправильный ход. попробуйте еще раз.')
                continue

            undo = input('хотите отменить последний ход или возвратиться на несколько ходов? (y/n/число): ')

            if undo.lower() == 'y':
                self.pop_moves()
                c -= 1
            elif undo.isdigit():
                count = int(undo)
                self.pop_moves(count)
                c -= count

        print('игра окончена. победили ', 'белые' if self.are_pieces_left(Color.white) else 'черные')

chess_board = Board()
chess_board.select_chess_set()