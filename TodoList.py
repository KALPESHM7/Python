TodoList=[]

def DisplayMenu():
    print("----------To Do List----------")
    print("1.Add Task")
    print("2.Mark as Completed")
    print("3.Delete")
    print("4.View Tasks")
    print("5.Exit")
    
def AddTask():
    content=input("Enter a Task to Add:")
    TodoList.append(content)
    print(f"Task {content} Added")
def View():
    if len(TodoList)== 0:
        print("No Task in list")
    else:
        print("\n Your Tasks")
        for i,task in enumerate(TodoList):
            print(f"{i+1}.{task}")
def Delete():# We use Try and except block because if delete is not working or if any error comes it can continue with the execution of the program.
    View() #The user to help choose 
    try:
        index=int(input("Enter the Number to Delete:"))-1
        if 0 <= index <= len(TodoList):
            deleted=TodoList.pop(index)
            print(f"Deleted Task")
        else:
            print("Invalid Number")
    except ValueError:
        print("Please Choose a Number")
    
    
    
def MaC():
    View() # To help thee user to decide which to MaC
    try:
        index1=int(input("Enter the Task number that need to mark as completed:"))-1
        if 0<= index1 <= len(TodoList):
            if "[Completed]" in TodoList[index1]:
                print("Task is already marked as Completed")
            else:
                TodoList[index1]=TodoList[index1]+" [Completed]"
                print("Task marked as completed,U can also delete the task that is completed")
        else:
            print("Invalid Task  Number")
    except ValueError:
        print("Choose a Number")
    
while True:
    DisplayMenu()
    choice =int(input("Enter your choice (1-5):"))
    
    if choice == 1:
        AddTask()
    elif choice == 2:
        MaC()
    elif choice == 3:
        Delete()
    elif choice == 4:
        View()
    elif choice == 5:
        break
    else:
        print("Invalid Choice! Choose a value between (1-5)")
        