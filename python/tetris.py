
import copy
from constants import COLOURS, BLACK, X, Y, ROTATION, FIXED


NUM_ROTATIONS = len(ROTATION)


def create_empty_row(num_columns):
    return [BLACK] * num_columns


def rotate_parts(parts, mode):
    r = ROTATION[mode % NUM_ROTATIONS]
    r_x = r[X]
    r_y = r[Y]
    new_parts = []

    for p in parts:
        x = p[X]
        y = p[Y]
        new_x = r_x[X] * x + r_x[Y] * y
        new_y = r_y[X] * x + r_y[Y] * y

        new_parts.append([new_x, new_y])

    return new_parts


class Tetris():
    def __init__(self, height, width, move_down_frames):
        self.height = height
        self. width = width
        self.board = []
        self.rotation_point = None
        self.piece_parts = None
        self.need_new_piece = True
        self.game_over = False
        self.score = 0
        self.num_frames = 0
        self.move_down_frames = move_down_frames
        for _ in range(height):
            self.board.append(create_empty_row(width))

    def in_play(self, x, y):
        in_x = x >= 0 and x < self.width
        in_y = y >= 0
        return in_x and in_y

    def y_valid(self, y):
        return y >= 0 and y < self.height

    def check_collision(self, rotation_point, piece_parts):

        origin_x = rotation_point[X]
        origin_y = rotation_point[Y]

        for relative in piece_parts:
            new_x = origin_x + relative[X]
            new_y = origin_y + relative[Y]

            if self.in_play(new_x, new_y):
                if self.y_valid(new_y) and self.board[new_y][new_x] != BLACK:
                    return True
            else:
                return True

        return False

    def rotate_piece(self, mode):
        new_parts = rotate_parts(self.piece_parts, mode)
        if not self.check_collision(self.rotation_point, new_parts):
            self.piece_parts = new_parts

    def move_piece_side(self, side_delta):
        new_rotation_point = [self.rotation_point[X] +
                              side_delta, self.rotation_point[Y]]
        if not self.check_collision(new_rotation_point, self.piece_parts):
            self.rotation_point = new_rotation_point

    def move_piece_down(self):
        new_rotation_point = [self.rotation_point[X], self.rotation_point[Y]-1]

        if not self.check_collision(new_rotation_point, self.piece_parts):
            self.rotation_point = new_rotation_point

        else:
            success, rows_changed = self.add_piece()

            if success:
                rows_to_erase = []
                for row in rows_changed:
                    if self.check_erasable_row(row):
                        rows_to_erase.append(row)

                self.erase_rows(rows_to_erase)

                self.piece_parts = []
                self.need_new_piece = True
            else:
                self.game_over = True

    def erase_rows(self, rows_to_erase):
        rows_to_erase.sort()
        num_rows_to_erase = len(rows_to_erase)
        self.score += num_rows_to_erase

        if num_rows_to_erase > 0:
            read_index = 0
            write_row = 0
            read_row = 0
            rows_to_erase.append(self.height)

            while read_index <= num_rows_to_erase:

                while read_index < num_rows_to_erase and rows_to_erase[read_index] == read_row:
                    read_index += 1
                    read_row += 1

                for r in range(read_row, rows_to_erase[read_index]):
                    self.board[write_row] = self.board[r]
                    write_row += 1

                read_row = rows_to_erase[read_index] + 1
                read_index += 1

            for r in range(write_row, self.height):
                self.board[r] = create_empty_row(self.width)

    def add_piece(self):
        origin_x = self.rotation_point[X]
        origin_y = self.rotation_point[Y]
        rows_changed = set()

        for relative in self.piece_parts:
            new_x = origin_x + relative[X]
            new_y = origin_y + relative[Y]
            if self.y_valid(new_y) and self.board[new_y][new_x] == BLACK:
                self.board[new_y][new_x] = FIXED
                rows_changed.add(new_y)
            else:
                return (False, [])

        return (True, rows_changed)

    def check_erasable_row(self, row_num):

        is_erasable = True
        column = 0
        row = self.board[row_num]

        while is_erasable and column < self.width:
            is_erasable = row[column] != BLACK
            column += 1

        return is_erasable

    def assign_new_piece(self, new_parts):

        if self.need_new_piece:
            self.piece_parts = new_parts
            self.rotation_point = self.place_piece(new_parts)
            self.need_new_piece = False

    def get_board_state(self):
        v = copy.deepcopy(self.board)
        origin_x = self.rotation_point[X]
        origin_y = self.rotation_point[Y]
        rows_changed = set()

        for relative in self.piece_parts:
            new_x = origin_x + relative[X]
            new_y = origin_y + relative[Y]
            self.board[new_y][new_x] = FIXED

    def place_piece(self, new_parts):

        max_y = 0
        for relative in self.piece_parts:
            max_y = max(max_y, relative[Y])

        return [self.width >> 1, self.height - 1 + max_y]

    def reset(self):
        self.score = 0

        for i in range(self.height):
            for j in range(self.width):
                self.board[i][j] = BLACK

        self.need_new_piece = True

    def loop(self, actions):

        if not (self.game_over or self.need_new_piece):

            if self.num_frames % self.move_down_frames == 0:
                # should move down
                pass

            # Based on actions you should move/ rotate the piece in a certain way
            pass
            self.num_frames += 1
        return (self.game_over, self.need_new_piece)
