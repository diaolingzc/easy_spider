try:
    with open('its.txt', 'w') as data:
        print("it's...", file=data)
except IOError as err:
    print('ioErr ' + str(err))

import pickle
# pickle.dump()
