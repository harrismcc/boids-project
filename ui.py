



def update_value(attr, value, centerBoid):
    for boid in centerBoid.phonebook.getAllBoids():
        setattr(boid, attr, value)

def speed_slider(s):
    #Update speed
    update_value('speed', s.value, s.centerBoid)
