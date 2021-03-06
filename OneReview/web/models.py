from django.db import models
from wordcloud import WordCloud
# import matplotlib.pyplot as plt
import os
from os import path
from io import StringIO
from web.processing import *
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
from matplotlib.dates import DateFormatter

import base64
from io import BytesIO

# Create your models here.
class User(models.Model):
    full_name = models.CharField(max_length=70)

class Cloud(models.Model):
    # get data directory (using getcwd() is needed to support running example in generated IPython notebook)
    def generate_cloud(cloud_path):
        # get path for wordcloud
        # d = path.dirname(__file__) if "__file__" in locals() else os.getcwd()

        # Read the whole text.
        # text = open(path.join(d, 'constitution.txt')).read()

        # Generate a word cloud image
        if len(cloud_path) is 0:
            cloud_path = "This product is the best best best. It gave me the biggliest of joy. This is a really good way to interface with the mainframe. I was super sweet, sweeter than just sweet. It's the best!"
        wordcloud = WordCloud().generate(cloud_path)

        image = wordcloud.to_image()
        
        #imgdata = StringIO()
        #image.imsave(imgdata, format='png')
        #imgdata.seek(0)
        
        #return image#imgdata
        buffered = BytesIO()
        image.save(buffered, format="JPEG")
        img_str = base64.b64encode(buffered.getvalue())
        return img_str

class GetAmazonReviews(models.Model):
    def getTextReviews(product):
        data = get_product_sentiment(product, 2)
        data_string = ''
        for row in data:
            for datum in row:
                data_string += datum
        return data_string
