
class Location():
    def __init__(self, left, right, up, down):
        self.left = left
        self.right = right
        self.up = up
        self.down = down
    
    def __str__(self):
        return "(l: {left}, r: {right}, u:{up}, d:{down})".format(
            left = self.left, right = self.right, up = self.up, down = self.down)
    
    def __repr__(self):
        return str(self)
