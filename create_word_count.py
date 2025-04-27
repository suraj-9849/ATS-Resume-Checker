import matplotlib.pyplot as plt
from wordcloud import WordCloud
import matplotlib.pyplot as plt

def create_word_cloud(text):
    """Create a word cloud from text"""
    wordcloud = WordCloud(
        width=800, height=400, background_color="white", max_words=100
    ).generate(text)

    fig, ax = plt.subplots(figsize=(10, 5))
    ax.imshow(wordcloud, interpolation="bilinear")
    ax.axis("off")

    return fig
