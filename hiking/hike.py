from bs4 import BeautifulSoup
import glob
from wordcloud import WordCloud
from collections import defaultdict as dd
import pickle


WORDINDEX_FILENAME = "wordindex.pkl"


def get_summary(divs):
    return divs[2].text.strip().split("\n")[0]


def get_location(divs):
    return divs[2].text.strip().split("\n")[1]


def read_hike_data(path):
    hikes = []
    hike2index = {}
    index2hike = {}
    index = 0
    for hike in glob.glob("%s/*.html" % path):
        soup = BeautifulSoup(open(hike), "html.parser")
        divs = soup.find_all("div", {"class": "w3-container"})
        hikes.append({"summary": get_summary(divs), "location": get_location(divs), "name": hike})
        hike2index[hike] = index
        index2hike[index] = hike
        index += 1

    return tuple(hikes), index2hike, hike2index


def create_wordcloud(path="hikes"):
    # TODO: save the image.
    import matplotlib.pyplot as plt

    hikes, _, _ = read_hike_data(path)
    text = " ".join([hike["summary"] for hike in hikes])
    with open("summary.txt", "wt") as f:
        f.write(text)

    wordcloud = WordCloud().generate(text)
    plt.imshow(wordcloud, interpolation="bilinear")
    plt.axis("off")

    # lower max_font_size
    # wordcloud = WordCloud(max_font_size=40).generate(text)
    # plt.figure()
    # plt.imshow(wordcloud, interpolation="bilinear")
    # plt.axis("off")
    # plt.show()


def build_word_index(hikes):
    word_index = dd(list)
    for i, hike in enumerate(hikes):
        for word in hike["summary"].lower().split():
            word_index[word].append(i)
    print(word_index)
    f = open(WORDINDEX_FILENAME, "wb")
    pickle.dump(word_index, f)

    return word_index


def load_or_build_word_index(hikes):
    try:
        f = open(WORDINDEX_FILENAME, "rb")
        print(f.name)
        return pickle.load(f)
    except Exception:
        return build_word_index(hikes)


def search(hikes, word_index, query):
    for hike_index in word_index[query]:
        print(hikes[hike_index]["summary"])


def run():
    hikes, index2hike, hike2index = read_hike_data(path="hikes")
    word_index = load_or_build_word_index(hikes)
    print(word_index["pleasant"])
    search(hikes, word_index, "awesome")


run()
