def compile_pairs_into_message(pairs):
    msg = ""
    for p in pairs:
        msg += p[0] + " : " + p[1] + "\n"
    return msg


# проверка работоспособности подпрограммы
if __name__ == "__main__":
    pairs = [
        ["кошка", "cat"],
        ["собака", "dog"],
        ["машина", "car"],
        ]
    msg = compile_pairs_into_message(pairs)
    print(msg)
