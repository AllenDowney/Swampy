turmite = Turmite(world)
for i in range(1000):
    if turmite.is_on_mark():
        turmite.rt()
    else:
        turmite.lt()
    turmite.toggle()
    turmite.fd()
