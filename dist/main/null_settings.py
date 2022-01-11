def set_null():
    f = open('score.txt', 'w')
    f.write('0')
    f.close()

    f = open('character.txt', 'w')
    f.write("first=True\nfirst_price=0\nsecond=False\nsecond_price=200\n")
    f.close()
