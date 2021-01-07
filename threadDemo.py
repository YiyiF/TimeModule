import threading, time
print('Start of program.')

def takeANap(str):
    time.sleep(5)
    print('Wake up, %s' % str)

threadObj = threading.Thread(target=takeANap, args=['FYY'])
threadObj.start()

print('End of program.')
