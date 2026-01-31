# 🗂️ CLI Task Manager – Python

A command-line based Task Manager application built using Python.  
This project supports full CRUD operations with data persistence using a JSON file and follows clean, modular, object-oriented design principles.

---

## 📌 Features

- Add new tasks with title, priority, and due date
- View all tasks in a structured tabular format
- Update task details (title, priority, due date)
- Mark tasks as completed
- Delete tasks using unique task IDs
- Filter tasks by:
  - Status (Pending / Completed)
  - Due date (Today / This Week)
- Persistent storage using JSON (tasks are not lost after program exit)
- Input validation and error handling

---

## 🛠️ Technologies Used

- **Python 3**
- **Object-Oriented Programming (OOP)**
- **UUID** for unique task identification
- **JSON** for data persistence
- **datetime module** for date validation and filtering

---

## 📂 Project Structure

```plaintext

├── task-manager/
    ├── TaskMAnager.py
    ├── .gitignore
    └── README.md

```

---

## ▶️ How to Run the Project

### 1️⃣ Clone the repository

```
git clone https://github.com/ybhavanareddy/cli-task-manager-python.git 
```
## 2️⃣ Navigate to the project folder
    
        cd task-manager
    

## 3️⃣ Run the application
    
        python TaskManager.py
    

## Example Usage

--- Task Manager ---
1. Add Task
2. View Tasks
3. Update Task
4. Mark Task as Complete
5. Delete Task
6. Filter Tasks
7. Exit

# Design Highlights

### Separation of Concerns

 - Task class → data model

 - TaskManager class → business logic

 - CLI menu → user interaction

### UUID-based Task IDs
- Ensures reliable update and   delete operations even after task reordering.

### JSON Persistence
- Tasks are automatically saved and loaded across program runs.

### Validation & Error Handling
- Prevents invalid priority values and incorrect date formats.

# License

- This project is for learning and demonstration purposes.

# 👩‍💻 Author

## Bhavana

🔗 LinkedIn
http://www.linkedin.com/in/yatham-bhavana
