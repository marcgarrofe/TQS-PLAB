import tkinter as tk
WINDOW_SIZE = "500x200"


class Vista:
    def __init__(self):
        # Init Tkinter
        self.gui = tk.Tk(className='card game')

        # Set Window Size
        self.gui.geometry(WINDOW_SIZE)

        # Call Main menu
        self.menu()

    def call_menu(self):
        self.clear_frame()
        self.menu()

    def menu(self):
        start_game_button = tk.Button(self.gui, text="Start Game")
        start_game_button.pack()
        ranking_button = tk.Button(self.gui, text="Ranking", command=self.call_ranking)
        ranking_button.pack()

    def call_ranking(self):
        self.clear_frame()
        self.ranking()

    def ranking(self):
        text = tk.Text(self.gui, height=8)
        text.pack()
        text.insert('1.0', 'This is a Text widget demo')
        back_to_menu_button = tk.Button(self.gui, text="Back to Menu", command=self.call_menu)
        back_to_menu_button.pack()

    def refresh(self):
        # Define window loop
        # self.gui.mainloop()
        self.gui.update_idletasks()
        self.gui.update()

    def clear_frame(self):
        for widgets in self.gui.winfo_children():
            widgets.destroy()
