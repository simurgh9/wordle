# Print the output of this function and redirect to
# a file, e. g., wrod_list.csv.
def correlate():
    # Bellow is the javascript source downloaded from
    # the Wordle website on 27 Feb 2022 to extract the
    # words.
    with open('main.4d41d2be.js') as fl:
        js = fl.read()
        js = js[js.index('Ma=[')+4:]
        js = js[:js.index(']')]
        words = js.strip().split(',')
        words = [w.strip()[1:-1] for w in words]

    # Bellow is the popular five words data downloaded
    # from Wolfram with their frequencies in English.
    with open('words.csv') as fl:
        freq = {}
        for line in fl.readlines():
            line = line.strip().split(',')
            freq[line[0]] = float(line[1])

    # These are words present in the list from
    # data/main.4d41d2be.js but absent from the Wolfram
    # data. I downloaded their frequencies from Wolfram
    # separately.
    with open('absent.csv') as fl:
        for line in fl.readlines():
            line = line.strip().split(',')
            freq[line[0]] = float(line[1])

    for word in words:
        print(f'{word},{freq[word]}')


if __name__ == '__main__':
    correlate()
