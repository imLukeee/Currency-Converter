import customtkinter as ctk
import requests
from settings import *
from ui_elements import *


class App(ctk.CTk):
    def __init__(self):
        super().__init__(fg_color=BG_COLOR)

        self.api_base_url = 'https://api.frankfurter.dev/v1/latest'

        #Window setup
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        x = (screen_width // 2) - (WINDOW_WIDTH // 2)
        y = (screen_height // 2) - (WINDOW_HEIIGHT // 2)

        self.minsize(MIN_WIDTH, MIN_HEIGHT)
        self.maxsize(MAX_WIDTH, MAX_HEIGHT)
        self.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIIGHT}+{x}+{y}')
        self.title('Currency converter')
        self.resizable(RESIZABLE[0], RESIZABLE[1])

        #fonts
        self.title_font = ctk.CTkFont('Arial', 48, 'bold')
        self.heading_font = ctk.CTkFont('Arial', 32, 'bold')
        self.widget_font = ctk.CTkFont('Arial', 28, 'normal')
        self.output_font = ctk.CTkFont('Trebuchet MS', 36, 'bold')
        
        #get current exchange rates from api
        self.get_current_exchange_rates()

        #variables
        self.user_input = ctk.StringVar(value='1')
        self.starting_currency = ctk.StringVar(value = self.currencies[0])
        self.target_currency = ctk.StringVar(value = self.currencies[1])
        self.converted_value = ctk.DoubleVar()
        self.output_string = ctk.StringVar()

        self.update_values()

        #Layout
        self.create_grid_layout()
        self.create_widgets()

        #tracing
        self.user_input.trace_add('write', self.validate_and_update)
        self.old_value = self.user_input.get()

        self.starting_currency.trace_add('write', self.update_values)
        self.target_currency.trace_add('write', self.update_values)

        #scaling
        self.bind('<Configure>', self._on_configure)
        
        #Run
        self.mainloop()


    def update_values(self, *args):
        if not self.user_input.get().isdigit():
            self.user_input.set(self.old_value)
            pass
        elif self.starting_currency.get() != 'EUR' and float(self.user_input.get()) != 0:
            base  = float(self.user_input.get()) / self.exchange_rates[self.starting_currency.get()]
            self.converted_value.set(round(base * self.exchange_rates[self.target_currency.get()],2))
            
        self.output_string.set(f'{self.user_input.get()} {self.starting_currency.get()}\n=\n{self.converted_value.get()} {self.target_currency.get()}')    


    def create_grid_layout(self):
        self.columnconfigure((0,1,2), weight=1, uniform='a')
        self.rowconfigure((0,1,2,3), weight=1, uniform='a')

    def create_widgets(self):
        Title_Frame(self, self.title_font)
        Amount_Input(self, self.user_input, self.heading_font, self.widget_font)
        Currency_selector(self, self.currencies, self.starting_currency, self.target_currency, self.swap_currencies, self.heading_font, self.widget_font)
        self.output_value_frame = Output_value_frame(self, self.output_string, self.output_font)

    def validate_input(self, *args):
        current = self.user_input.get()
        if not current.isnumeric():
            if current == '':
                self.old_value = ''
            else:
                self.user_input.set(self.old_value)
                current = self.old_value
        elif len(current) <= MAX_INPUT_LENGTH:
            self.old_value = current
        else:
            print(f'Old: {self.old_value}, current: {current}')
            self.user_input.set(self.old_value)

    def get_current_exchange_rates(self):
        response = requests.get(self.api_base_url)

        if response.status_code == 200:
            self.exchange_rates = response.json()['rates']
            self.currencies = list(self.exchange_rates.keys())

    def swap_currencies(self):
        temp = self.target_currency.get()
        self.target_currency.set(self.starting_currency.get())
        self.starting_currency.set(temp)

    def validate_and_update(self, *args):
        current = self.user_input.get()

        if not current.isnumeric():
            if current == '':
                self.old_value = ''
            else:
                self.user_input.set(self.old_value)
            return  # Abort update if invalid input

        elif len(current) <= MAX_INPUT_LENGTH:
            self.old_value = current
        else:
            self.user_input.set(self.old_value)
            return  # Abort update if too long

        self.update_values()

    def scale_fonts(self):
        new_title_size = min(max(24, int(self.winfo_width() * 0.075)), 72)
        new_heading_size = min(max(24, int(self.winfo_width() * 0.05)), 36)
        new_output_size = min(max(24, int(self.winfo_width() * 0.05)), 40)
        new_widget_size = min(max(18, int(self.winfo_width() * 0.04)), 32)

        self.title_font.configure(size = new_title_size)
        self.output_font.configure(size = new_output_size)
        self.heading_font.configure(size = new_heading_size)
        self.widget_font.configure(size = new_widget_size)

        self.update_idletasks()

    def _on_configure(self, event):
        if event.widget == self:
            self.scale_fonts()
            

if __name__ == '__main__':
    App()