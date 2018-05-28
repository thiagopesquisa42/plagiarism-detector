from Entity.Seeding.SeedAttributes import SeedAttributes

class Seed():
    def __init__(self,
        suspiciousSentence,
        sourceSentence):
        self.suspiciousSentence = suspiciousSentence
        self.sourceSentence = sourceSentence
        self.attributes = SeedAttributes()
        self.detection = None
