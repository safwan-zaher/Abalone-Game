#The Button class represents a graphical button element that can be displayed on a screen or user interface.
class Button():
    #The __init__ method initializes a Button object with various attributes such as 
    #image (the image to be displayed on the button), 
    #pos (the position of the button on the screen),
    #text_input (the text displayed on the button), 
    #font (the font used for the text), 
    #base_color (the color of the text when not hovered), and 
    #hovering_color (the color of the text when the mouse hovers over the button).
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color) # renders the text_input using the font and assigns the rendered text surface to the text attribute.
		if self.image is None:
			self.image = self.text
            #These lines create rectangular bounding boxes (rect and text_rect) for the image and text surfaces, 
            #respectively. The center argument specifies the position of the center of the rectangle.
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))
        
 #This line defines the update method of the Button class. It takes a screen parameter, which represents the graphical display or screen where the button will be updated.
	def update(self, screen):
		if self.image is not None:
            #This condition checks if the image attribute is not None. If it's not None, it blits (renders) the image surface onto the screen at the position specified by the rect attribute.
		    screen.blit(self.image, self.rect)
            
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
        #This line defines the checkForInput method of the Button class. 
        #It takes a position parameter, which represents the position to be checked (usually the mouse cursor position).
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)