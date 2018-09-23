from django.db import models
from wordcloud import WordCloud
# import matplotlib.pyplot as plt
import os
from os import path

# Create your models here.
class User(models.Model):
    full_name = models.CharField(max_length=70)

class Cloud(models.Model):
    # get data directory (using getcwd() is needed to support running example in generated IPython notebook)
    def generate_cloud(cloud_text):
        # get path for wordcloud
        # d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

        # Read the whole text.
        # text = open(path.join(d, 'constitution.txt')).read()

        # Generate a word cloud image
        wordcloud = WordCloud().generate(text)

        image = wordcloud.to_image()
        image.show()