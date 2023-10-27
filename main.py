
# from kivy.config import Config
# Config.set('kivy','keyboard_mode','systemanddock')

from kivy.lang import Builder
from kivy.metrics import dp

from kivymd.app import MDApp
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.snackbar import Snackbar
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.screen import MDScreen

from kivymd.font_definitions import theme_font_styles

# from kivymd.font_definitions import

from kivy.core.window import Window
Window.size=(910,600)


KV = '''
MDBoxLayout:
    md_bg_color: "mediumorchid"
    orientation: "vertical"
    padding:25,15
    spacing:"10dp"
    
    MDTopAppBar:
        
        title: "Шпаргалка по Git"
        theme_text_color:"Custom"
        specific_text_color: "mediumorchid"
        elevation: 3
        shadow_color: "black"
        
        md_bg_color:"yellow"
        left_action_items: [["menu", lambda x: app.callback(x)]]
        # opposite_colors: True
        
        
    MDLabel:
        id:label
        adaptive_size: True
        pos_hint: {"center_x": .5, "top": 1}
        text: "Главная страница"
        theme_text_color:"Custom"
        text_color: "yellow"
        font_size:"25sp"
        padding: "0dp", "15dp","0dp","0dp"
        halign: "center"
    
    MDData:
        id: table_screen
           
    MDRaisedButton:
        elevation: 3
        shadow_color: "black"
        font_size: "20sp"
        text_color: "white"
        line_color: "yellow"
        line_width:2
        md_bg_color:"mediumorchid"
        size_hint:0.3,0.1
        pos_hint: {"center_x": .5, "y": 1}
        text: "Показать команды"
        on_press: table_screen.del_rows()
        on_release: table_screen.add_rows(label.text)
        
        # on_release: table_screen.add_rows([f'{label.text}'])
'''

# работаю с таблицей
class MDData(MDScreen):

    #внешний вид при инициализации
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.data_tables = MDDataTable(
            rows_num=50,
            background_color_header="mediumorchid",
            background_color_cell="orchid",
            background_color_selected_cell="mediumorchid",

            column_data=[
                ("[size=18][color=#FFFFFF]Описание команды[/color][/size]", dp(80)),
                ("[size=18][color=#FFFFFF]Команда[/color][/size]", dp(100))
            ]
        )
        self.add_widget(self.data_tables)

    # добавляю строки, в зависимости от выбора меню
    def add_rows(self,x):
        title_str=x
        number_file=''
        count=0
        match title_str:
            case 'Настройка Git':
                number_file=str(1)
            case 'Локальный репозиторий':
                number_file = str(2)
            case 'Глобальный репозиторий':
                number_file = str(3)
            case 'Индекс. Коммит':
                number_file = str(4)
            case 'Работа с ветками':
                number_file = str(5)
            case 'Файл .gitignore':
                number_file = str(6)
            case 'История изменений':
                number_file = str(7)
            case 'Отмена/удаление':
                number_file = str(8)
            case 'Прочее':
                number_file = str(9)
        if number_file=='':
            pass
        else:
            with open(number_file+'.txt',encoding='utf-8') as file:
                s=file.readlines()
                i=0
                while i <(len(s)-1):
                    self.data_tables.add_row([("[size=16][color=#FFFFFF]"+s[i][:len(s[i])-1]+"[/color][/size]"),
                                              ("[size=18][color=#FFFF00]"+s[i+1][:len(s[i+1])-1]+"[/color][/size]")])
                    i+=2
    def del_rows(self):
       while len(self.data_tables.row_data)>0:
           self.data_tables.remove_row(self.data_tables.row_data[-1])



class MainApp(MDApp):
    def build(self):
        menu_items = [
            {
                "text": f"{i}",
                "font_size": 20,
                "text_color":"white",
                "divider_color":"white",
                "md_bg_color":"mediumorchid",
                "leading_icon": "git",
                "leading_icon_color": "yellow",
                "on_release": lambda x=f"{i}": self.menu_callback(x),
            } for i in ["Настройка Git", "Локальный репозиторий", "Глобальный репозиторий",
                        "Индекс. Коммит", "Работа с ветками", "Файл .gitignore", "История изменений",
                        "Отмена/удаление", "Прочее"]
        ]
        self.menu = MDDropdownMenu(items=menu_items)
        return Builder.load_string(KV)

    def callback(self, button):
        self.menu.caller = button
        self.root.ids.table_screen.del_rows()
        self.root.ids.label.text = "Главное меню"
        self.menu.open()

    def menu_callback(self,x):

        self.root.ids.label.text=f'{x}'
       

if __name__=='__main__':
    MainApp().run()