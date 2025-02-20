import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QPushButton,
    QLabel, QLineEdit, QComboBox, QListWidget, QListWidgetItem, QMessageBox, QDialog, QGraphicsDropShadowEffect
)
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtCore import Qt

# -------------------------------
# Language Dictionary
# -------------------------------
LANGUAGES = {
    "English": {
        "window_title": "To-Do List Manager",
        "add_task": "Add Task",
        "edit_task": "Edit Task",
        "delete_task": "Delete Task(s)",
        "mark_as_complete": "Mark as Complete",
        "light_mode": "Light Mode",
        "dark_mode": "Dark Mode",
        "search_placeholder": "Search Task...",
        "filter_priority": "Filter by Priority:",
        "filter_status": "Filter by Status:",
        "sort_tasks": "Sort Tasks:",
        "priority_filter_options": ["All", "High", "Medium", "Low"],
        "status_filter_options": ["All", "Completed", "Incomplete"],
        "sort_options": ["None", "Priority"],
        "error": "Error",
        "please_provide_task": "Please provide both a task description and a date.",
        "edit_info": "Please select exactly one task to edit.",
        "task_not_found": "Task not found.",
        "delete_info": "Please select at least one task to delete.",
        "mark_done_info": "Please select at least one task to toggle.",
        "add_task_dialog_title": "Add Task",
        "edit_task_dialog_title": "Edit Task",
        "task_description": "Task Description:",
        "priority": "Priority:",
        "date": "Date (YYYY-MM-DD):",
        "save_changes": "Save Changes",
        "add": "Add Task",
        "completed": "Completed",
        "incomplete": "Incomplete",
        "high_priority": "High",
        "medium_priority": "Medium",
        "low_priority": "Low"
    },
    "Arabic": {
        "window_title": "مدير قائمة المهام",
        "add_task": "إضافة مهمة",
        "edit_task": "تعديل المهمة",
        "delete_task": "حذف المهمة(المهام)",
        "mark_as_complete": "تمييز كمكتملة",
        "light_mode": "الوضع الفاتح",
        "dark_mode": "الوضع الداكن",
        "search_placeholder": "ابحث عن مهمة...",
        "filter_priority": "تصفية حسب الأولوية:",
        "filter_status": "تصفية حسب الحالة:",
        "sort_tasks": "ترتيب المهام:",
        "priority_filter_options": ["الكل", "عالي", "متوسط", "منخفض"],
        "status_filter_options": ["الكل", "مكتملة", "غير مكتملة"],
        "sort_options": ["لا شيء", "الأولوية"],
        "error": "خطأ",
        "please_provide_task": "يرجى تقديم وصف المهمة والتاريخ.",
        "edit_info": "يرجى اختيار مهمة واحدة للتعديل.",
        "task_not_found": "المهمة غير موجودة.",
        "delete_info": "يرجى اختيار مهمة واحدة على الأقل للحذف.",
        "mark_done_info": "يرجى اختيار مهمة واحدة على الأقل لتبديل حالتها.",
        "add_task_dialog_title": "إضافة مهمة",
        "edit_task_dialog_title": "تعديل المهمة",
        "task_description": "وصف المهمة:",
        "priority": "الأولوية:",
        "date": "التاريخ (YYYY-MM-DD):",
        "save_changes": "حفظ التغييرات",
        "add": "إضافة المهمة",
        "completed": "مكتملة",
        "incomplete": "غير مكتملة",
        "high_priority": "عالي",
        "medium_priority": "متوسط",
        "low_priority": "منخفض"
    }
}

# -------------------------------
# Data Structures for Task Management
# -------------------------------
class TaskNode:
    def __init__(self, description, priority, date):
        self.description = description   # Task description
        self.priority = priority         # Priority: High, Medium, Low
        self.date = date                 # Date as a string (e.g., "2025-02-18")
        self.completed = False           # Completion status
        self.next = None                 # Pointer to the next task

class TaskList:
    def __init__(self):
        self.head = None  # Start of the linked list

    def add_task(self, description, priority, date):
        new_task = TaskNode(description, priority, date)
        if not self.head:
            self.head = new_task
        else:
            current = self.head
            while current.next:
                current = current.next
            current.next = new_task

    def delete_task(self, description):
        if not self.head:
            return
        if self.head.description == description:
            self.head = self.head.next
            return
        prev = self.head
        current = self.head.next
        while current:
            if current.description == description:
                prev.next = current.next
                return
            prev = current
            current = current.next

    def toggle_task_status(self, description):
        current = self.head
        while current:
            if current.description == description:
                current.completed = not current.completed
                break
            current = current.next

    def edit_task(self, old_description, new_description, new_priority, new_date):
        current = self.head
        while current:
            if current.description == old_description:
                current.description = new_description
                current.priority = new_priority
                current.date = new_date
                break
            current = current.next

    def get_all_tasks(self):
        tasks = []
        current = self.head
        while current:
            tasks.append((current.description, current.priority, current.date, current.completed))
            current = current.next
        return tasks

# -------------------------------
# Dialog for Adding a New Task
# -------------------------------
class AddTaskDialog(QDialog):
    def __init__(self, parent=None, language="English"):
        super().__init__(parent)
        self.language = language
        self.setWindowTitle(LANGUAGES[self.language]["add_task_dialog_title"])
        self.setFixedSize(350, 250)
        self.setStyleSheet("""
            QDialog { background-color: #34495e; color: #ecf0f1; }
            QLabel { font-size: 14px; }
            QLineEdit, QComboBox { border: 2px solid #3498db; border-radius: 8px; padding: 5px; }
            QLineEdit { background-color: #ecf0f1; color: #2c3e50; }
            QComboBox { background-color: #ecf0f1; color: #2c3e50; }
            QPushButton { background-color: #2980b9; border: none; border-radius: 8px; color: white; padding: 10px; }
            QPushButton:hover { background-color: #3498db; }
        """)
        layout = QVBoxLayout()

        self.desc_label = QLabel(LANGUAGES[self.language]["task_description"])
        layout.addWidget(self.desc_label)
        self.desc_edit = QLineEdit()
        layout.addWidget(self.desc_edit)

        self.priority_label = QLabel(LANGUAGES[self.language]["priority"])
        layout.addWidget(self.priority_label)
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["High", "Medium", "Low"])
        layout.addWidget(self.priority_combo)

        self.date_label = QLabel(LANGUAGES[self.language]["date"])
        layout.addWidget(self.date_label)
        self.date_edit = QLineEdit()
        self.date_edit.setPlaceholderText("e.g., 2025-02-18")
        layout.addWidget(self.date_edit)

        self.add_button = QPushButton(LANGUAGES[self.language]["add"])
        self.add_button.clicked.connect(self.accept)
        layout.addWidget(self.add_button)

        self.setLayout(layout)

    def get_data(self):
        return self.desc_edit.text(), self.priority_combo.currentText(), self.date_edit.text()

# -------------------------------
# Dialog for Editing a Task
# -------------------------------
class EditTaskDialog(QDialog):
    def __init__(self, parent=None, description="", priority="High", date="", language="English"):
        super().__init__(parent)
        self.language = language
        self.setWindowTitle(LANGUAGES[self.language]["edit_task_dialog_title"])
        self.setFixedSize(350, 250)
        self.setStyleSheet("""
            QDialog { background-color: #34495e; color: #ecf0f1; }
            QLabel { font-size: 14px; }
            QLineEdit, QComboBox { border: 2px solid #3498db; border-radius: 8px; padding: 5px; }
            QLineEdit { background-color: #ecf0f1; color: #2c3e50; }
            QComboBox { background-color: #ecf0f1; color: #2c3e50; }
            QPushButton { background-color: #2980b9; border: none; border-radius: 8px; color: white; padding: 10px; }
            QPushButton:hover { background-color: #3498db; }
        """)
        layout = QVBoxLayout()

        self.desc_label = QLabel(LANGUAGES[self.language]["task_description"])
        layout.addWidget(self.desc_label)
        self.desc_edit = QLineEdit()
        self.desc_edit.setText(description)
        layout.addWidget(self.desc_edit)

        self.priority_label = QLabel(LANGUAGES[self.language]["priority"])
        layout.addWidget(self.priority_label)
        self.priority_combo = QComboBox()
        self.priority_combo.addItems(["High", "Medium", "Low"])
        self.priority_combo.setCurrentText(priority)
        layout.addWidget(self.priority_combo)

        self.date_label = QLabel(LANGUAGES[self.language]["date"])
        layout.addWidget(self.date_label)
        self.date_edit = QLineEdit()
        self.date_edit.setText(date)
        layout.addWidget(self.date_edit)

        self.save_button = QPushButton(LANGUAGES[self.language]["save_changes"])
        self.save_button.clicked.connect(self.accept)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

    def get_data(self):
        return self.desc_edit.text(), self.priority_combo.currentText(), self.date_edit.text()

# -------------------------------
# Main Application Window
# -------------------------------
class ToDoApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.language = "English"  # Default language
        self.dark_mode = True      # Start in dark mode
        self.task_list = TaskList()  # Linked list for tasks

        # Define stylesheets:
        # Dark Mode: Purple & Black
        self.dark_style = """
            QMainWindow {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #000000, stop:1 #800080);
            }
            QLabel {
                color: #ffffff;
                font-size: 14px;
            }
            QPushButton {
                background-color: #800080;
                border: none;
                border-radius: 8px;
                color: white;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #9932CC;
            }
            QLineEdit, QComboBox {
                border: 2px solid #800080;
                border-radius: 8px;
                padding: 5px;
            }
            QLineEdit {
                background-color: #2c2c2c;
                color: #ffffff;
            }
            QComboBox {
                background-color: #2c2c2c;
                color: #ffffff;
            }
            QListWidget {
                background-color: #2c2c2c;
                border: none;
                padding: 5px;
                border-radius: 8px;
                color: #ffffff;
            }
        """
        # Light Mode: Blue & Grey
        self.light_style = """
            QMainWindow {
                background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 #3b5998, stop:1 #8b9dc3);
            }
            QLabel {
                color: #2c3e50;
                font-size: 14px;
            }
            QPushButton {
                background-color: #3b5998;
                border: none;
                border-radius: 8px;
                color: white;
                padding: 10px;
            }
            QPushButton:hover {
                background-color: #2c3e50;
            }
            QLineEdit, QComboBox {
                border: 2px solid #3b5998;
                border-radius: 8px;
                padding: 5px;
            }
            QLineEdit {
                background-color: white;
                color: #2c3e50;
            }
            QComboBox {
                background-color: white;
                color: #2c3e50;
            }
            QListWidget {
                background-color: white;
                border: none;
                padding: 5px;
                border-radius: 8px;
                color: #2c3e50;
            }
        """
        self.initUI()
        self.apply_theme()
        self.update_language()

    def initUI(self):
        self.setFont(QFont("Segoe UI", 10))
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.main_layout = QVBoxLayout(self.central_widget)

        # --- Language Selection Layout ---
        self.lang_layout = QHBoxLayout()
        self.english_button = QPushButton("English")
        self.english_button.clicked.connect(lambda: self.set_language("English"))
        self.lang_layout.addWidget(self.english_button)
        self.arabic_button = QPushButton("العربية")
        self.arabic_button.clicked.connect(lambda: self.set_language("Arabic"))
        self.lang_layout.addWidget(self.arabic_button)
        self.main_layout.addLayout(self.lang_layout)

        # --- Top Button Layout ---
        self.button_layout = QHBoxLayout()
        self.add_button = QPushButton()
        self.add_button.clicked.connect(self.open_add_task_dialog)
        self.button_layout.addWidget(self.add_button)

        self.edit_button = QPushButton()
        self.edit_button.clicked.connect(self.edit_task)
        self.button_layout.addWidget(self.edit_button)

        self.delete_button = QPushButton()
        self.delete_button.clicked.connect(self.delete_tasks)
        self.button_layout.addWidget(self.delete_button)

        self.done_button = QPushButton()
        self.done_button.clicked.connect(self.toggle_tasks_status)
        self.button_layout.addWidget(self.done_button)

        self.light_mode_button = QPushButton()
        self.light_mode_button.clicked.connect(self.set_light_mode)
        self.button_layout.addWidget(self.light_mode_button)

        self.dark_mode_button = QPushButton()
        self.dark_mode_button.clicked.connect(self.set_dark_mode)
        self.button_layout.addWidget(self.dark_mode_button)
        self.main_layout.addLayout(self.button_layout)

        # --- Search and Filter Layout ---
        self.search_box = QLineEdit()
        self.search_box.textChanged.connect(self.update_task_display)
        self.main_layout.addWidget(self.search_box)

        self.filter_priority_label = QLabel()
        self.main_layout.addWidget(self.filter_priority_label)
        self.filter_priority_combo = QComboBox()
        self.main_layout.addWidget(self.filter_priority_combo)
        self.filter_priority_combo.currentIndexChanged.connect(self.update_task_display)

        self.filter_status_label = QLabel()
        self.main_layout.addWidget(self.filter_status_label)
        self.filter_status_combo = QComboBox()
        self.main_layout.addWidget(self.filter_status_combo)
        self.filter_status_combo.currentIndexChanged.connect(self.update_task_display)

        self.sort_tasks_label = QLabel()
        self.main_layout.addWidget(self.sort_tasks_label)
        self.sort_combo = QComboBox()
        self.main_layout.addWidget(self.sort_combo)
        self.sort_combo.currentIndexChanged.connect(self.update_task_display)

        # --- Task List Widget ---
        self.tasks_list_widget = QListWidget()
        self.tasks_list_widget.setSelectionMode(QListWidget.ExtendedSelection)
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(15)
        shadow.setXOffset(3)
        shadow.setYOffset(3)
        shadow.setColor(QColor(0, 0, 0, 160))
        self.tasks_list_widget.setGraphicsEffect(shadow)
        self.main_layout.addWidget(self.tasks_list_widget)

        self.update_task_display()

    def apply_theme(self):
        if self.dark_mode:
            self.setStyleSheet(self.dark_style)
        else:
            self.setStyleSheet(self.light_style)

    def set_dark_mode(self):
        self.dark_mode = True
        self.apply_theme()

    def set_light_mode(self):
        self.dark_mode = False
        self.apply_theme()

    def set_language(self, lang):
        self.language = lang
        self.update_language()
        self.update_task_display()

    def update_language(self):
        self.setWindowTitle(LANGUAGES[self.language]["window_title"])
        self.add_button.setText(LANGUAGES[self.language]["add_task"])
        self.edit_button.setText(LANGUAGES[self.language]["edit_task"])
        self.delete_button.setText(LANGUAGES[self.language]["delete_task"])
        self.done_button.setText(LANGUAGES[self.language]["mark_as_complete"])
        self.light_mode_button.setText(LANGUAGES[self.language]["light_mode"])
        self.dark_mode_button.setText(LANGUAGES[self.language]["dark_mode"])
        self.search_box.setPlaceholderText(LANGUAGES[self.language]["search_placeholder"])
        self.filter_priority_label.setText(LANGUAGES[self.language]["filter_priority"])
        self.filter_status_label.setText(LANGUAGES[self.language]["filter_status"])
        self.sort_tasks_label.setText(LANGUAGES[self.language]["sort_tasks"])
        self.filter_priority_combo.clear()
        self.filter_priority_combo.addItems(LANGUAGES[self.language]["priority_filter_options"])
        self.filter_status_combo.clear()
        self.filter_status_combo.addItems(LANGUAGES[self.language]["status_filter_options"])
        self.sort_combo.clear()
        self.sort_combo.addItems(LANGUAGES[self.language]["sort_options"])

    def open_add_task_dialog(self):
        dialog = AddTaskDialog(self, language=self.language)
        if dialog.exec_():
            description, priority, date = dialog.get_data()
            if description.strip() == "" or date.strip() == "":
                QMessageBox.warning(self, LANGUAGES[self.language]["error"], LANGUAGES[self.language]["please_provide_task"])
                return
            self.task_list.add_task(description, priority, date)
            self.update_task_display()

    def edit_task(self):
        selected_items = self.tasks_list_widget.selectedItems()
        if len(selected_items) != 1:
            QMessageBox.information(self, LANGUAGES[self.language]["error"], LANGUAGES[self.language]["edit_info"])
            return
        # Retrieve the full description stored in the item data
        item = selected_items[0]
        old_description = item.data(Qt.UserRole)
        task_to_edit = None
        for task in self.task_list.get_all_tasks():
            if task[0] == old_description:
                task_to_edit = task
                break
        if task_to_edit is None:
            QMessageBox.information(self, LANGUAGES[self.language]["error"], LANGUAGES[self.language]["task_not_found"])
            return
        dialog = EditTaskDialog(self, description=task_to_edit[0], priority=task_to_edit[1], date=task_to_edit[2], language=self.language)
        if dialog.exec_():
            new_description, new_priority, new_date = dialog.get_data()
            if new_description.strip() == "" or new_date.strip() == "":
                QMessageBox.warning(self, LANGUAGES[self.language]["error"], LANGUAGES[self.language]["please_provide_task"])
                return
            self.task_list.edit_task(old_description, new_description, new_priority, new_date)
            self.update_task_display()

    def delete_tasks(self):
        selected_items = self.tasks_list_widget.selectedItems()
        if not selected_items:
            QMessageBox.information(self, LANGUAGES[self.language]["error"], LANGUAGES[self.language]["delete_info"])
            return
        for item in selected_items:
            description = item.data(Qt.UserRole)
            self.task_list.delete_task(description)
        self.update_task_display()

    def toggle_tasks_status(self):
        selected_items = self.tasks_list_widget.selectedItems()
        if not selected_items:
            QMessageBox.information(self, LANGUAGES[self.language]["error"], LANGUAGES[self.language]["mark_done_info"])
            return
        for item in selected_items:
            description = item.data(Qt.UserRole)
            self.task_list.toggle_task_status(description)
        self.update_task_display()

    def update_task_display(self):
        tasks = self.task_list.get_all_tasks()
        priority_emojis = {"High": "🔥", "Medium": "⭐", "Low": "🟢"}
        status_emojis = {True: "✅", False: "❌"}
        search_text = self.search_box.text().strip().lower()
        if search_text:
            tasks = [task for task in tasks if search_text in task[0].lower()]
        priority_filter = self.filter_priority_combo.currentText()
        if priority_filter != LANGUAGES[self.language]["priority_filter_options"][0]:
            tasks = [task for task in tasks if task[1] == priority_filter or
                     (priority_filter == LANGUAGES[self.language]["high_priority"] and task[1] == "High") or
                     (priority_filter == LANGUAGES[self.language]["medium_priority"] and task[1] == "Medium") or
                     (priority_filter == LANGUAGES[self.language]["low_priority"] and task[1] == "Low")]
        status_filter = self.filter_status_combo.currentText()
        if status_filter != LANGUAGES[self.language]["status_filter_options"][0]:
            if status_filter == LANGUAGES[self.language]["completed"]:
                tasks = [task for task in tasks if task[3]]
            elif status_filter == LANGUAGES[self.language]["incomplete"]:
                tasks = [task for task in tasks if not task[3]]
        sort_option = self.sort_combo.currentText()
        if sort_option == LANGUAGES[self.language]["sort_options"][1]:
            order = {"High": 1, "Medium": 2, "Low": 3}
            tasks = sorted(tasks, key=lambda x: order.get(x[1], 99))
        self.tasks_list_widget.clear()
        for task in tasks:
            priority_map = {
                "High": LANGUAGES[self.language]["high_priority"],
                "Medium": LANGUAGES[self.language]["medium_priority"],
                "Low": LANGUAGES[self.language]["low_priority"]
            }
            prio_display = priority_map.get(task[1], task[1])
            status_text = LANGUAGES[self.language]["completed"] if task[3] else LANGUAGES[self.language]["incomplete"]
            s_emoji = status_emojis.get(task[3], "")
            item_text = f"{task[0]} {priority_emojis.get(task[1], '')} - {prio_display} - {task[2]} - {status_text} {s_emoji}"
            list_item = QListWidgetItem(item_text)
            list_item.setData(Qt.UserRole, task[0])
            self.tasks_list_widget.addItem(list_item)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ToDoApp()
    window.show()
    sys.exit(app.exec_())
