import Image, ImageDraw, random, scene

def generate_shapes(num_circles = random.randint(4, 5)):
    shapes = []
    for i in xrange(num_circles):
        x = i * 20 - ((num_circles/2)*30)  #-60, -40, etcto +20
        y = (random.random()-0.5) * 30   #-15 to +15
        rad = random.randint(50, 100)
        shapes.append([x, y, rad])
    return shapes

def cloud_maker():
    num_circles = random.randint(4, 5)
    #pil coord system 0,0 is bot left.  scene is top left.  
    #  so, need to flip old y convention, add h
    #  also top/bottom y get reversed in order.
    #  finally, since scene let you draw out of the frame, we need to offset the coord sys by the min values of x and y 
    h=100+15+5   #bottom corner rad=100, plus 15 that old cloud went up, plus 5 for shadow
    x0=60 +2 # to push first ellipse into view
    y0=15+5 # since old code shifted white up by 5, this was max top coord
    image_size = (100+x0, h) 
    theImage = Image.new('RGBA', image_size) #, 'pink')
    draw = ImageDraw.Draw(theImage)
    
    circles = generate_shapes(num_circles)
    for i in circles:
        bbox = (i[0]+x0, h-y0-i[2] , i[2]+x0, h-y0-i[1]+5)
        draw.ellipse(bbox, fill='rgb(90%,90%,90%)')
    for i in circles:
        bbox = (i[0]+x0, h-y0-i[2] , i[2]+x0,h-y0- i[1]-5)
        draw.ellipse(bbox, fill='white')

    del draw
    return theImage

class Cloud(scene.Layer):
    def __init__(self, parent = None):
        cloud_image = cloud_maker()
        super(self.__class__, self).__init__(scene.Rect(*cloud_image.getbbox()))
        if parent:
            parent.add_layer(self)
        self.image = scene.load_pil_image(cloud_image)

class MyScene(scene.Scene):
    def __init__(self):
        scene.run(self)

    def setup(self):
        self.cloud = Cloud(self)
        self.cloud.frame.x = 0
        self.cloud.frame.y = self.bounds.h * 0.8

    def draw(self):
        scene.background(0.40, 0.80, 1.00)
        self.root_layer.update(self.dt)
        self.root_layer.draw()
        self.cloud.frame.x += 1
        if not self.bounds.intersects(self.cloud.frame):
            del self.cloud  # whack the old cloud
            self.setup()    # and create a new one

MyScene()
