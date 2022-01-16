from reconize import book_reconize


def set_coordinate(left, upper, right, lower):
    coordinate = dict(left=left, upper=upper, right=right, lower=lower)
    return coordinate


if __name__ == '__main__':
    coordinate = set_coordinate(52, 1545, 1048, 1668)
    bookdir = ""

    book_reconize(bookdir, coordinate)
