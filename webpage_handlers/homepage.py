# Python Libraries
import random

# GAE Libraries
from google.appengine.ext import db

# Utility classes
from handlerBase import Handler

# Database Models
from imageInfo import ImageInfo

class HomepageHandler(Handler):
    def renderPage(self):
        # Get the images to display on the webpage
        imagesQueryInstance = db.GqlQuery("SELECT * FROM ImageInfo")
        images = []
        for image in imagesQueryInstance:
            images.append(image)
        
        
        imagesToRender = []
        imageNumber = 0
        
        # Loop while images remain and at most three times
        while len(images) > 0 and imageNumber < 3:
            # Get a random index for the image list
            index = random.randint(0, len(images) - 1)
            
            # Add the image to the render list and remove from the master list
            imagesToRender.append(images[index])
            images.pop(index)
            
            # Incriment the counter
            imageNumber += 1
            
        # Try to get three photos
        photo0 = ""
        photo1 = ""
        photo2 = ""
        try:
            photo0 = imagesToRender[0]
            photo1 = imagesToRender[1]
            photo2 = imagesToRender[2]
        except:
            pass
    
        self.render('homepage.html', photo0=photo0, photo1=photo1,
            photo2=photo2)

    def get(self):
        self.renderPage()