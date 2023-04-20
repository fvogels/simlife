class Grid:
    def __init__(self, width, height, initializer):
        assert width > 0
        assert height > 0
        self.__contents = [
            [
                initializer(x, y) for x in range(width)
            ]
            for y in range(height)
        ]

    @property
    def width(self):
        return len(self.__contents[0])

    @property
    def height(self):
        return len(self.__contents)

    def __getitem__(self, position):
        assert self.is_valid_position(position)
        return self.__contents[position.y][position.x]

    def is_valid_position(self, position):
        return 0 <= position.x < self.width and 0 <= position.y < self.height
