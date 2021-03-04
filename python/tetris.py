

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
    def __init__(self, height, width):
        self.height = height
        self. width = width
        self.board = []
        self.rotation_point = None
        self.piece_parts = None
        self.need_new_piece = True
        self.game_over = False
        for _ in range(height):
            self.board.append(create_empty_row(width))

    def in_bounds(self, x, y):
        in_x = x >= 0 and x < self.width
        in_y = y >= 0 and y < self.height
        return in_x and in_y

    def check_collision(self, rotation_point, piece_parts):

        origin_x = rotation_point[X]
        origin_y = rotation_point[Y]

        for part in piece_parts:
            relative_x = part[X]
            relative_y = part[Y]

            new_x = origin_x + relative_x
            new_y = origin_y + relative_y

            if self.in_bounds(new_x, new_y):
                if self.board[new_y][new_x] != BLACK:
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

        for part in self.piece_parts:
            relative_x = part[X]
            relative_y = part[Y]
            new_x = origin_x + relative_x
            new_y = origin_y + relative_y
            if self.board[new_y][new_x] == BLACK:
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

    def assign_new_piece(self, new_rotation_point, new_parts):

        if self.need_new_piece:
            self.rotation_point = new_rotation_point
            self.piece_parts = new_parts
            self.need_new_piece = False
