import json
from datetime import datetime, timedelta
from uuid import uuid4

class Task:
    def __init__(self, title, priority, due_date, status="Pending", task_id=None):
        self.id = task_id if task_id else str(uuid4())
        self.title = title
        self.priority = priority
        self.due_date = due_date
        self.status = status

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'priority': self.priority,
            'due_date': self.due_date,
            'status': self.status
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            title=data['title'],
            priority=data['priority'],
            due_date=data['due_date'],
            status=data['status'],
            task_id=data['id']
        )

class TaskManager:
    def __init__(self):
        self.task_list = []
        self.load_from_file()

    def add_task(self, title, priority, due_date):
        if priority not in ['Low', 'Medium', 'High']:
            raise ValueError("Priority must be Low, Medium, or High")
        
        try:
            datetime.strptime(due_date, '%Y-%m-%d')
        except ValueError:
            raise ValueError("Due date must be in YYYY-MM-DD format")
        
        task = Task(title, priority, due_date)
        self.task_list.append(task)
        self.save_to_file()
        return task

    def view_tasks(self, filter_type=None, filter_value=None):
        if not self.task_list:
            print("No tasks available.")
            return
        
        tasks_to_display = self.task_list
        
        if filter_type == 'status':
            tasks_to_display = [t for t in self.task_list if t.status == filter_value]
        elif filter_type == 'due_date':
            today = datetime.now().date()
            if filter_value == 'today':
                tasks_to_display = [t for t in self.task_list 
                                  if datetime.strptime(t.due_date, '%Y-%m-%d').date() == today]
            elif filter_value == 'week':
                end_of_week = today + timedelta(days=7)
                tasks_to_display = [t for t in self.task_list 
                                  if today <= datetime.strptime(t.due_date, '%Y-%m-%d').date() <= end_of_week]
        
        print("\n{:<36} {:<20} {:<10} {:<12} {:<10}".format(
            "ID", "Title", "Priority", "Due Date", "Status"))
        print("-" * 90)
        for task in tasks_to_display:
            print("{:<36} {:<20} {:<10} {:<12} {:<10}".format(
                task.id, task.title, task.priority, task.due_date, task.status))
        print()

    def update_task(self, task_id, **kwargs):
        task = self._find_task(task_id)
        if not task:
            print("Task not found.")
            return False
        
        for key, value in kwargs.items():
            if hasattr(task, key):
                if key == 'priority' and value not in ['Low', 'Medium', 'High']:
                    print("Invalid priority. Must be Low, Medium, or High.")
                    return False
                elif key == 'due_date':
                    try:
                        datetime.strptime(value, '%Y-%m-%d')
                    except ValueError:
                        print("Invalid date format. Use YYYY-MM-DD.")
                        return False
                setattr(task, key, value)
        
        self.save_to_file()
        return True

    def mark_complete(self, task_id):
        task = self._find_task(task_id)
        if task:
            task.status = 'Completed'
            self.save_to_file()
            return True
        return False

    def delete_task(self, task_id):
        task = self._find_task(task_id)
        if task:
            self.task_list.remove(task)
            self.save_to_file()
            return True
        return False

    def filter_tasks(self, by, value):
        if by == 'status':
            return [t for t in self.task_list if t.status == value]
        elif by == 'due_date':
            today = datetime.now().date()
            if value == 'today':
                return [t for t in self.task_list 
                       if datetime.strptime(t.due_date, '%Y-%m-%d').date() == today]
            elif value == 'week':
                end_of_week = today + timedelta(days=7)
                return [t for t in self.task_list 
                       if today <= datetime.strptime(t.due_date, '%Y-%m-%d').date() <= end_of_week]
        return []

    def save_to_file(self):
        with open('tasks.json', 'w') as f:
            json.dump([task.to_dict() for task in self.task_list], f, indent=2)

    def load_from_file(self):
        try:
            with open('tasks.json', 'r') as f:
                data = json.load(f)
                self.task_list = [Task.from_dict(task_data) for task_data in data]
        except FileNotFoundError:
            self.task_list = []

    def _find_task(self, task_id):
        for task in self.task_list:
            if task.id == task_id:
                return task
        return None

def display_menu():
    print("\nTaskForge - Task Manager")
    print("1. Add Task")
    print("2. View Tasks")
    print("3. Update Task")
    print("4. Mark Task as Complete")
    print("5. Delete Task")
    print("6. Filter Tasks")
    print("7. Exit")

def get_user_input(prompt, validation_func=None):
    while True:
        try:
            user_input = input(prompt).strip()
            if validation_func and not validation_func(user_input):
                raise ValueError("Invalid input")
            return user_input
        except ValueError as e:
            print(f"Error: {e}. Please try again.")

def main():
    manager = TaskManager()
    
    while True:
        display_menu()
        choice = get_user_input("Enter your choice (1-7): ", lambda x: x in ['1', '2', '3', '4', '5', '6', '7'])
        
        if choice == '1':  # Add Task
            print("\nAdd New Task")
            title = get_user_input("Title: ", lambda x: len(x) > 0)
            priority = get_user_input("Priority (Low/Medium/High): ", 
                                    lambda x: x.lower() in ['low', 'medium', 'high']).capitalize()
            due_date = get_user_input("Due Date (YYYY-MM-DD): ", 
                                     lambda x: bool(datetime.strptime(x, '%Y-%m-%d')))
            
            manager.add_task(title, priority, due_date)
            print("Task added successfully!")
            
        elif choice == '2':  # View Tasks
            print("\nView Tasks")
            print("1. View All")
            print("2. View Pending")
            print("3. View Completed")
            view_choice = get_user_input("Enter your choice (1-3): ", lambda x: x in ['1', '2', '3'])
            
            if view_choice == '1':
                manager.view_tasks()
            elif view_choice == '2':
                manager.view_tasks(filter_type='status', filter_value='Pending')
            elif view_choice == '3':
                manager.view_tasks(filter_type='status', filter_value='Completed')
                
        elif choice == '3':  # Update Task
            manager.view_tasks()
            task_id = get_user_input("Enter task ID to update: ")
            
            print("\nLeave blank to keep current value")
            title = get_user_input(f"New Title: ")
            priority = get_user_input("New Priority (Low/Medium/High): ", 
                                    lambda x: x == '' or x.lower() in ['low', 'medium', 'high'])
            if priority:
                priority = priority.capitalize()
            due_date = get_user_input("New Due Date (YYYY-MM-DD): ", 
                                    lambda x: x == '' or bool(datetime.strptime(x, '%Y-%m-%d')))
            
            updates = {}
            if title: updates['title'] = title
            if priority: updates['priority'] = priority
            if due_date: updates['due_date'] = due_date
            
            if updates and manager.update_task(task_id, **updates):
                print("Task updated successfully!")
            else:
                print("No updates made or task not found.")
                
        elif choice == '4':  # Mark Complete
            manager.view_tasks(filter_type='status', filter_value='Pending')
            task_id = get_user_input("Enter task ID to mark as complete: ")
            
            if manager.mark_complete(task_id):
                print("Task marked as complete!")
            else:
                print("Task not found.")
                
        elif choice == '5':  # Delete Task
            manager.view_tasks()
            task_id = get_user_input("Enter task ID to delete: ")
            
            if manager.delete_task(task_id):
                print("Task deleted successfully!")
            else:
                print("Task not found.")
                
        elif choice == '6':  # Filter Tasks
            print("\nFilter Tasks")
            print("1. By Status")
            print("2. By Due Date (Today)")
            print("3. By Due Date (This Week)")
            filter_choice = get_user_input("Enter your choice (1-3): ", lambda x: x in ['1', '2', '3'])
            
            if filter_choice == '1':
                status = get_user_input("Enter status (Pending/Completed): ", 
                                      lambda x: x.lower() in ['pending', 'completed']).capitalize()
                manager.view_tasks(filter_type='status', filter_value=status)
            elif filter_choice == '2':
                manager.view_tasks(filter_type='due_date', filter_value='today')
            elif filter_choice == '3':
                manager.view_tasks(filter_type='due_date', filter_value='week')
                
        elif choice == '7':  # Exit
            print("Saving tasks and exiting...")
            manager.save_to_file()
            break

if __name__ == "__main__":
    main()