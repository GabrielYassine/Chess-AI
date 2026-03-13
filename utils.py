def move_to_text(move):
    files = "abcdefgh"

    if len(move) == 5:
        r1, c1, r2, c2, special = move
    else:
        r1, c1, r2, c2 = move
        special = None

    start = files[c1] + str(8 - r1)
    end = files[c2] + str(8 - r2)

    if special is None:
        return start + end

    return start + end + " (" + special + ")"


def text_to_move(text, legal_moves):
    text = text.strip().lower()

    files = "abcdefgh"

    if len(text) != 4:
        return None

    try:
        c1 = files.index(text[0])
        r1 = 8 - int(text[1])
        c2 = files.index(text[2])
        r2 = 8 - int(text[3])
    except:
        return None

    for move in legal_moves:
        if len(move) == 5:
            mr1, mc1, mr2, mc2, special = move
        else:
            mr1, mc1, mr2, mc2 = move
            special = None

        if (r1, c1, r2, c2) == (mr1, mc1, mr2, mc2):
            return move

    return None