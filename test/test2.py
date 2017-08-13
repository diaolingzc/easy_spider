__author__ = 'Gallon'

try:
    data=open('missing.txt')
    print(data.readline(), end='')
except IOError as err:
    print('File error' + str(err))
finally:
    if 'data' in locals():
        data.close()