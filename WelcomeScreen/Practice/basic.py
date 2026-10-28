if __name__ == '__main__':
    N = int(input("Enter N: "))
    arr = []
    while N > 0:
        command = input()
        print(type(command))

        if command == "append":
            arr.append(int(command))

        elif command == "insert":
            arr.insert(int(command), int(command))

        elif command == "remove":
            arr.remove((int(command)))

        elif command == "sort":
            arr.sort()

        elif command == "pop":
            arr.pop()

        elif command == "reverse":
            arr.reverse()

        elif command == "print":
            print(arr)

        N -= 1
