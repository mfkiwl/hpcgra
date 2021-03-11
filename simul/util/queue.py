# TODO DESCRIPTION AND COMMENTS
# TODO TO_STRING
class Queue:

    def __init__(self):
        self.__queue_content = []

    def clear(self):
        self.__queue_content = []

    def get_peek(self):
        if self.get_size() > 0:
            return self.__queue_content[0]
        else:
            raise Exception("Error! The queue is empty.")

    def is_empty(self):
        return len(self.__queue_content) == 0

    def get(self):
        if self.is_empty():
            raise Exception("Error! The queue is empty.")
        data = self.__queue_content[0]
        self.__queue_content.pop(0)
        return data

    def put(self, data):
        self.__queue_content.append(data)

    def get_size(self):
        return len(self.__queue_content)
