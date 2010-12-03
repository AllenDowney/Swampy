def draw(t, dist, n):
    fd(t, dist)
    lt(t)
    draw(t, dist, n-1)

bob = Turtle(world)
bob.delay = 0
draw(bob, 50, 4)
