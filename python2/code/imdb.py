import os
import re

def open_gunzip(filename):
    """open the filename, using a pipe and gunzip to read a
    compressed file without uncompressing the whole thing."""
    cmd = 'gunzip -c ' + filename
    fp = os.popen(cmd)
    return fp

def process_file(filename, f, num=float('Inf')):
    """read the given filename and extract information;
    for each film, call f() with string arguments:
    actor, date, title, role """
    
    fp = open_gunzip(filename)
    i = 0

    # skip over the header until you get to the following magic line
    for line in fp:
        if line.strip() == '----			------':
            break

    # regexp to recognize actor, tabs, movie
    split1 = re.compile('([^\t]*)\t*(.*)', re.UNICODE)

    # regexp to recognize title, date, role
    split2 = re.compile('([^\(]*)\s*(\([^\)]*\))[^\[]*(\[[^\]]*\])?', 
                        re.UNICODE)

    # regexp to recognize television (TV), video (V), video game (VG)
    video = re.compile('\(T?V|VG\)', re.U)

    actor = ''
    for line in fp:
        line = line.rstrip()
        if line == '': continue
        if line[0] == '-': break

        # split the line into actor info and movie info;
        # keep track of the current actor
        ro = split1.match(line)
        if ro:
            new_actor, info = ro.groups()
            if new_actor:
                actor = new_actor
        else:
            print 'BAD1', line
            continue

        # skip television shows (titles in quotation marks)
        if info[0] == '"':
            continue

        # skip made for TV and straight to video
        if video.search(info):
            continue

        # split the info into title, date and role
        ro = split2.match(info)
        if ro:
            title, date, role = ro.groups()
            if date == None:
                print 'BAD2', line
                continue

            f(actor, date, title, role)
            i += 1
            if i > num: break
        else:
            print 'BAD3', line
            continue

    stat = fp.close()


if __name__ == '__main__':

    def print_info(actor, date, title, role):
        print actor, date, title, role

    process_file('actors.list.gz', print_info)
