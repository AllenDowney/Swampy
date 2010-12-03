class Time: pass

def make_time(seconds):
    # given the number of seconds since midnight, build
    # a Time object with attributes hours, minutes and seconds
    time = Time()
    time.hours = seconds/3600
    seconds -= time.hours * 3600
    time.minutes = seconds/60
    seconds -= time.minutes * 60
    time.seconds = seconds
    return time

def print_time(t):
    print '%.2d:%.2d:%.2d' % (t.hours, t.minutes, t.seconds)

def convert_to_seconds(t):
    # take a Time object and compute the number of seconds
    # since midnight
    minutes = t.hours * 60 + t.minutes
    seconds = minutes * 60 + t.seconds
    return seconds

def add_times(t1, t2):
    seconds = convert_to_seconds(t1) + convert_to_seconds(t2)
    return make_time(seconds)

# if a movie starts at noon...
noon_time = make_time(12 * 60 * 60)

# and the run time of the movie is 109 minutes...
movie_minutes = 109
run_time = make_time(movie_minutes * 60)

# what time does the movie end?
end_time = add_times(noon_time, run_time)
print_time(end_time)
