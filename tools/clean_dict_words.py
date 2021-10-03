word = input()

if (word.isalpha() and len(word) > 10):
    new_word = word[1:-1]
    new_len = len(new_word)

    new_string = word[0] + str(new_len) + word[-1]

    print(new_string)
elif (word.isalpha()):
    print(word)
