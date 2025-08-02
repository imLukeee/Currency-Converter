import customtkinter as ctk
from settings import *

class Title_Frame(ctk.CTkFrame):
    def __init__(self, parent, font):
        super().__init__(master = parent, fg_color='transparent')
        self.grid(column = 0, columnspan = 3, row = 0, sticky = 'nsew')

        self.title_label = ctk.CTkLabel(self, text='Currency converter', font = font, text_color=TEXT_COLOR)
        self.title_label.place(relx = 0.5, rely = 0.5, anchor = 'center', relwidth = 1, relheight = 1)


class Amount_Input(ctk.CTkFrame):
    def __init__(self, parent, user_input, title_font, input_font):
        super().__init__(master=parent, fg_color='transparent')
        self.grid(column = 0, columnspan = 3, row = 1, sticky = 'nsew')

        self.instruction_label = ctk.CTkLabel(self, text='Enter Amount', text_color=TEXT_COLOR, font = title_font)
        self.input_box = ctk.CTkEntry(self, corner_radius = 10, fg_color = ACCENT_COLOR, text_color = TEXT_COLOR,font = input_font, textvariable=user_input)

        self.instruction_label.place(relx = 0.15, rely = 0.25, anchor = 'w', relheight = 0.25)
        self.input_box.place(relx = 0.15, rely = 0.55, relwidth = 0.7, relheight = 0.3, anchor = 'w')


class Currency_selector(ctk.CTkFrame):
    def __init__(self, parent, values, starting_var, target_var, swap_func, title_font, option_font):
        super().__init__(master = parent, fg_color='transparent')
        self.grid(column = 0, columnspan = 3, row = 2, sticky = 'nsew')

        self.from_label = ctk.CTkLabel(self, text_color = TEXT_COLOR, font = title_font, text = 'From')
        self.to_label = ctk.CTkLabel(self, text_color = TEXT_COLOR, font = title_font, text = 'To')

        self.starting_curr_selector = Currency_dropdown_menu(self, values, starting_var, option_font)
        self.ending_curr_selector = Currency_dropdown_menu(self, values, target_var, option_font)

        self.currency_swap_button = ctk.CTkButton(self, text = '⇆', font = ctk.CTkFont('Arial', 24),command=swap_func, fg_color = ACCENT_COLOR, text_color = TEXT_COLOR, hover = True, hover_color = HOVER_COLOR_DARK, corner_radius = 10)

        self.from_label.place(relx = 0.15, rely = 0.3, anchor = 'w', relheight = 0.25)
        self.to_label.place(relx = 0.6, rely = 0.3, anchor = 'w', relheight = 0.25)

        self.starting_curr_selector.place(relx = 0.15, rely = 0.55, relwidth = 0.25, relheight = 0.25, anchor = 'w')
        self.currency_swap_button.place(relx = 0.55, rely = 0.55, relwidth = 0.10, relheight = 0.25, anchor = 'e')
        self.ending_curr_selector.place(relx = 0.85, rely = 0.55, relwidth = 0.25, relheight = 0.25, anchor = 'e')


class Currency_dropdown_menu(ctk.CTkOptionMenu):
    def __init__(self, parent, values, variable, font):
        super().__init__(master = parent, corner_radius = 10, fg_color = ACCENT_COLOR, button_color = ACCENT_COLOR, hover = True, button_hover_color = HOVER_COLOR_DARK, text_color = TEXT_COLOR, font = font, dropdown_font = ctk.CTkFont('Arial', 14, 'bold'), values = values, variable = variable)


class Output_value_frame(ctk.CTkFrame):
    def __init__(self, parent, variable, font):
        super().__init__(master = parent, fg_color = 'transparent')
        self.grid(column = 0, columnspan = 3, row = 3, sticky = 'nsew')

        self.converted_equation_label = ctk.CTkLabel(self, text_color = TEXT_COLOR, font = font, textvariable = variable)

        self.converted_equation_label.place(relx = 0, rely = 0.05, anchor = 'nw', relwidth = 1)
