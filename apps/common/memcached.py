import memcache
mc=memcache.Client(["127.0.0.1:11211"])
def setmem(key,value,time=0):
    mc.set(key=key,val=value,time=time)

def getmem(key):
    return mc.get(key=key)
def delete(key):
    return mc.delete(key)