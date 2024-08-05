import threading

## The simple function that will simply print hello world and
## the thread that is executing this
def my_task():
    print("Hello World: {}".format(threading.current_thread()))

## We create our first thread and pass in our myTask function
## as its target
myFirstThread = threading.Thread(target=my_task)
## We start out thread
myFirstThread.start()