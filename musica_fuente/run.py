import sys, time, importlib
mod = importlib.import_module(sys.argv[1])
for f in mod.ALL:
    if len(sys.argv) > 2 and f.__name__ not in sys.argv[2:]: continue
    t=time.time(); d=f(); print(f.__name__, round(d,1), 's', round(time.time()-t,1), 'render', flush=True)
