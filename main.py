from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.uix.image import Image
from kivy.uix.floatlayout import FloatLayout


class MoneyManager(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # خلفية ملونة جميلة
        from kivy.graphics import Color, Rectangle
        with self.canvas.before:
            Color(0.4, 0.5, 0.7, 1)  # لون أزرق جميل
            self.rect = Rectangle(size=self.size, pos=self.pos)
        self.bind(size=self._update_rect, pos=self._update_rect)

        # القوائم والبيانات
        self.data = {}

        # الطبقة الأمامية
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        self.add_widget(main_layout)

        # صف الإدخال
        input_layout = BoxLayout(size_hint_y=None, height=50, spacing=5)

        self.name_input = TextInput(hint_text="الاسم", multiline=False)
        self.add_input = TextInput(hint_text="إضافة مبلغ", multiline=False, input_filter='float')
        self.sub_input = TextInput(hint_text="خصم مبلغ", multiline=False, input_filter='float')

        add_button = Button(text="حفظ / تعديل", on_press=self.add_or_update)

        input_layout.add_widget(self.name_input)
        input_layout.add_widget(self.add_input)
        input_layout.add_widget(self.sub_input)
        input_layout.add_widget(add_button)

        main_layout.add_widget(input_layout)

        # منطقة العرض (السجل)
        self.scroll = ScrollView()
        self.grid = GridLayout(cols=3, size_hint_y=None, spacing=5, padding=5)
        self.grid.bind(minimum_height=self.grid.setter('height'))
        self.scroll.add_widget(self.grid)
        main_layout.add_widget(self.scroll)

        # تحديث العرض المبدئي
        self.update_display()

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size

    def add_or_update(self, instance):
        name = self.name_input.text.strip()
        if not name:
            return

        add_val = self.add_input.text.strip()
        sub_val = self.sub_input.text.strip()

        add_amount = float(add_val) if add_val else 0
        sub_amount = float(sub_val) if sub_val else 0

        change = add_amount - sub_amount

        if name in self.data:
            self.data[name] += change
        else:
            self.data[name] = change

        # تنظيف الخانات
        self.name_input.text = ""
        self.add_input.text = ""
        self.sub_input.text = ""

        self.update_display()

    def edit_record(self, instance):
        """تحميل البيانات في خانات الإدخال لتعديلها"""
        name = instance.name
        self.name_input.text = name
        self.add_input.text = ""
        self.sub_input.text = ""

    def update_display(self):
        self.grid.clear_widgets()

        # عنوان الأعمدة
        self.grid.add_widget(Label(text="[b]الاسم[/b]", markup=True))
        self.grid.add_widget(Label(text="[b]الإجمالي[/b]", markup=True))
        self.grid.add_widget(Label(text="[b]تعديل[/b]", markup=True))

        for name, total in self.data.items():
            self.grid.add_widget(Label(text=name))
            self.grid.add_widget(Label(text=f"{total:.2f}"))

            edit_btn = Button(text="✏️", size_hint_y=None, height=30)
            edit_btn.name = name
            edit_btn.bind(on_press=self.edit_record)
            self.grid.add_widget(edit_btn)


class MoneyApp(App):
    def build(self):
        return MoneyManager()


if __name__ == "__main__":
    MoneyApp().run()
