VERSION = (0, 3, 2, 'final')

def get_version():
    v = "%d.%d.%d" % VERSION[:3]
    if VERSION[3] != 'final':
        v = "%s%s%d" % (v, VERSION[3], VERSION[4])
    return v
