class Entity:
    def __init__(self, x, y, health, damage):#constructeur : initialise les attributs
        self.x = x
        self.y = y
        self.health = health
        self.max_health = health
        self.damage = damage

    #coordonnees
    def set_x(self, x):
        self.x = x

    def get_x(self):
        return self.x
    
    def set_y(self, y):
        self.y = y

    def get_y(self):
        return self.y

    #combats
    def get_health(self):
        return self.health
    
    def set_health(self, health):
        self.health = health

    def get_max_health(self):
        return self.max_health

    def set_max_health(self, max_health):
        self.max_health = max_health

    def is_alive(self):
        return self.health > 0
    
    def gain_health(self, qty_health):
        self.health += qty_health
        if self.health > self.max_health:#on corrige le nb de pt de vie si celui-ci est superieur au maximum
            self.health = self.max_health
    
    def lose_health(self, qty_health):
        self.health -= qty_health
        if self.health < 0:#on corrige le nb de pt de vie si celui-ci est negatif
            self.health = 0

    def get_damage(self):
        return self.damage
    
    def set_damage(self, damage):
        self.damage = damage