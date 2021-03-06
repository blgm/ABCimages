# Module containing the Imagegenerator class which overlays text on images.
# It takes a list of images, a list of text, and a list of user genereated
# text locations as arguments.

import os, glob, random
from PIL import Image, ImageDraw, ImageFont # Install Pillow, not PIL

class Imagegenerator():
    def __init__(self, data_list, user_preferences):
        self.overlayimage_list(data_list, user_preferences)

    def overlayimage_list(self, data_list, user_preferences):
        self.image_list, self.text_list = data_list
        self.user_preferences = user_preferences
        self.font_file_list = glob.glob(os.path.join("fonts", "*.ttf"))
        random.shuffle(self.font_file_list)

        for i in range(len(self.text_list)):
            if user_preferences["font"] == "random":
                self.font_file = self.font_file_list[i % len(self.font_file_list)]
            else:
                self.font_file = os.path.join("fonts", user_preferences["font"])
            self.overlayimage(self.image_list[i], self.text_list[i], self.user_preferences, self.font_file)
     
    def overlayimage(self, image, text, user_preferences, font_file):
        self.myimage = image
        self.mytext = text
        self.font_size = user_preferences["font_size"]
        self.original_image = Image.open(os.path.join("photos", self.myimage + ".jpg")).convert("RGBA")
        self.x, self.y, self.font_size, self.max_width = 10, 10, self.font_size, self.original_image.size[0] - 20
        self.text_placeholder = Image.new("RGBA", self.original_image.size, (255,255,255,0))
        self.font = ImageFont.truetype(self.font_file, self.font_size)
        self.d = ImageDraw.Draw(self.text_placeholder)
        self.line = ""
        self.lines = []

        self.words = self.mytext.split() # Split by whitespace
        for word in self.words:
            if len(self.line.split()) == 0:
                self.line = word
            else:
                self.line = "{} {}".format(self.line, word)
            self.line_width, self.line_height = self.d.textsize(self.line, font = self.font)
            if self.line_width > self.max_width:
                self.lines.append({"width": self.line_width, "height": self.line_height, "string": self.line.rsplit(" ", 1)[0]})
                self.line = self.line.rsplit(" ", 1)[-1]
        self.lines.append({"width": self.line_width, "height": self.line_height, "string": self.line}) # Catch the last line

        for i, self.line in enumerate(self.lines):
            self.d.text((self.x, self.y + (i * self.lines[i-1]["height"])), self.line["string"], font = self.font, fill = (255,255,255,128)) # To justify right, would set x to original_image.size[0] - line["width"]

        self.out = Image.alpha_composite(self.original_image, self.text_placeholder)
        self.out.save(os.path.join("photos", self.myimage+".edit.jpg"))
