# http://127.0.0.1:61324/
import flet 
from flet import Page,Text,TextField,FloatingActionButton,Column,Row,text,IconButton,OutlinedButton,Tabs,Tab,UserControl,colors,icons,Checkbox

class Task(UserControl):
    def __init__(self, task_name, task_status_change, task_delete):
        super().__init__()
        self.completed = False
        self.task_name = task_name
        self.task_status_change = task_status_change
        self.task_delete = task_delete

    def build(self):
        self.display_task = Checkbox(
            value=False, label=self.task_name, on_change=self.status_changed
        )
        self.edit_name = TextField(expand=1)

        self.display_view = Row(
            alignment="spaceBetween",
            vertical_alignment="center",
            controls=[
                self.display_task,
                Row(
                    spacing=0,
                    controls=[
                        IconButton(
                            icon=icons.CREATE_OUTLINED,
                            tooltip="Edit To-Do",
                            on_click=self.edit_clicked,
                        ),
                        IconButton(
                            icons.DELETE_OUTLINE,
                            tooltip="Delete To-Do",
                            on_click=self.delete_clicked,
                        ),
                    ],
                ),
            ],
        )

        self.edit_view = Row(
            visible=False,
            alignment="spaceBetween",
            vertical_alignment="center",
            controls=[
                self.edit_name,
                IconButton(
                    icon=icons.DONE_OUTLINE_OUTLINED,
                    icon_color=colors.GREEN,
                    tooltip="Update To-Do",
                    on_click=self.save_clicked,
                ),
            ],
        )

        return Column(controls=[self.display_view, self.edit_view])

    def edit_clicked(self, e):
        self.edit_name.value = self.display_task.label
        self.display_view.visible = False
        self.edit_view.visible = True
        self.update()

    def save_clicked(self, e):
        self.display_task.label = self.edit_name.value
        self.display_view.visible = True
        self.edit_view.visible = False
        self.update()
    def delete_clicked(self, e):
        self.task_delete(self)

    def status_changed(self, e):
        self.completed = self.display_task.value
        self.task_status_change(self)

class MyTodoApp(UserControl):
    def build(self):
        # return Text("todo app") 
        self.new_task =TextField(hint_text="Add you task you wan to do", expand =True)
        self.tasks =Column()
        self.filter = Tabs(
            selected_index=0,
            on_change=self.tabs_changed,
            tabs=[Tab(text="All"), Tab(text="Active"), Tab(text="Completed")],
        )

        self.items_left = Text("No items left")
        return Column(
            width =600,
            controls=[
                Row([Text(value="Todos" , style ="headlineMedium")],alignment="center"),
                Row(
                    controls=[
                        self.new_task,
                        FloatingActionButton(icon=icons.ADD, on_click=self.add_clicked),
                    ]
                ),
                Column(
                    spacing=25,
                    controls=[
                        self.filter,
                        self.tasks,
                        Row(
                            alignment="spaceBetween",
                            vertical_alignment="center",
                            controls=[
                                self.items_left,
                                OutlinedButton(
                                    text="Clear completed", on_click=self.clear_clicked
                                ),
                            ],
                        ),
                    ],
                ),
            ],

        )
    def add_clicked(self,e):
        # print("add clicked")
        task = Task(self.new_task.value, self.task_status_change, self.task_delete)
        self.tasks.controls.append(task)
        self.new_task.value=""
        self.update()

    def task_status_change(self, task):
        self.update()
    def task_delete(self,task):
        self.tasks.controls.remove(task)
        self.update()
    def tabs_changed(self, e):
        self.update()

    def clear_clicked(self, e):
        for task in self.tasks.controls[:]:
            if task.completed:
                self.task_delete(task)


    def update(self):
        status =self.filter.tabs[self.filter.selected_index].text
        count = 0
        for task in self.tasks.controls:
            task.visible=(
                status =="All"
                or (status=="Active" and not task.completed)
                or (status == "Completed" and task.completed)
            )
            if not task.completed:
                count= count+1
        self.items_left.value = f"{count} active items(s) left"
        super().update()

def main(page: Page):
    page.title = "Todo App"
    page.horizontal_alignment = "center"

    # creat a TODO app instance
    app = MyTodoApp()

    page.add(app)


#target=main means calling the main function
#view=flet.WEB_BROWSER on which platform you want to run the app
# Local server http://127.0.0.1:61324/
flet.app(target=main,view=flet.WEB_BROWSER) 
