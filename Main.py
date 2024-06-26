from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput

class MainApp(App):
    def build(self):
        self.operators = ["/", "*", "+", "-"]
        self.last_was_operator = None
        self.last_button = None

        main_layout = BoxLayout(orientation="vertical")

        self.solution = TextInput(multiline=False, readonly=True, halign="right", font_size=55)
        main_layout.add_widget(self.solution)

        buttons = [
            ["7", "8", "9", "/"],
            ["4", "5", "6", "*"],
            ["1", "2", "3", "-"],
            [".", "0", "C", "+"],
            ["Clear", "⌫", "="]
        ]

        for row in buttons:
            h_layout = BoxLayout()
            for label in row:
                button = Button(text=label, pos_hint={"center_x": 0.5, "center_y": 0.5})
                if label != "=":
                    button.bind(on_press=self.on_button_press)
                else:
                    button.bind(on_press=self.on_solution)
                h_layout.add_widget(button)
            main_layout.add_widget(h_layout)

        return main_layout

    def on_button_press(self, instance):
        current = self.solution.text
        button_text = instance.text

        if button_text == "C":
            # Clear the solution widget
            self.solution.text = ""
        elif button_text == "⌫":
            # Backspace
            if current:
                self.solution.text = current[:-1]
        else:
            if current and (self.last_was_operator and button_text in self.operators):
                # Don’t add two operators right after each other
                return
            elif current == "" and button_text in self.operators:
                # First character cannot be an operator
                return
            else:
                new_text = current + button_text
                self.solution.text = new_text
                self.last_button = button_text
                self.last_was_operator = self.last_button in self.operators

    def on_solution(self, instance):
        text = self.solution.text
        if text:
            try:
                solution = str(eval(self.solution.text))
                self.solution.text = solution
            except Exception as e:
                self.solution.text = "Error"
                print("Error:", e)

if __name__ == "__main__":
    MainApp().run()
