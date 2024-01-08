"""
File: gui.py
Description: Graphical user interface for the password manager
Author: Justin Thoreson
Date: January 2024
"""

from password_generator import PasswordGenerator
from logger import Logger
from typing import Any, Callable
from pyglet import font
from sys import maxsize
import tkinter as tk

TITLE = 'Password Manager'
WIDTH = 500
HEIGHT = 400
PRIMARY_COLOR = '#222222'
SECONDARY_COLOR = '#cccccc'
PRIMARY_FONT = 'EmbossedBlackWide'
SECONDARY_FONT = 'TkTextFont'
HEADING_FONT_SIZE = 32
SUBHEADING_FONT_SIZE = 18
TEXT_FONT_SIZE = 10
PADDING = 10
ICON_FILEPATH = 'assets/images/pm.ico'
LOG_FILENAME = 'log'

class GUI(object):
    """Represents all graphical user interface functionality."""

    def __init__(self) -> None:
        """Configures the GUI."""

        font.add_file(f'assets/fonts/{PRIMARY_FONT}.ttf')
        self.__init_window()
        self.__init_window_content()
    
    def __init_window(self) -> None:
        """Creates a window."""

        self.__window = Window(TITLE, WIDTH, HEIGHT)

    def __init_window_content(self) -> None:
        """Sets the window content."""

        Heading(self.__window, TITLE, width=WIDTH, height=75, bg=PRIMARY_COLOR, fg=SECONDARY_COLOR, font=(PRIMARY_FONT, HEADING_FONT_SIZE))
        log = Log(self.__window, width=WIDTH / 2, height=325, bg=PRIMARY_COLOR, fg=SECONDARY_COLOR, padx=PADDING, pady=PADDING)
        Generator(self.__window, log.add, width=WIDTH / 2, height=325, bg=PRIMARY_COLOR, fg=SECONDARY_COLOR, padx=PADDING, pady=PADDING)

    def render(self) -> None:
        """Runs the GUI."""

        self.__window.render()

class Window(tk.Tk):
    """Represents a window."""

    def __init__(self, title: str, width: float, height: float) -> None:
        """Configures the window."""

        super().__init__()
        self.title(title)
        self.resizable(False, False)
        self.__icon()
        self.__size(width, height)
        self.__center()

    def __icon(self) -> None:
        """Sets the window icon."""

        self.iconbitmap(ICON_FILEPATH)

    def __size(self, width: float, height: float) -> None:
        """
        Sets the size of the window.
        :param width: The width of the window
        :param height: The height of the window
        """

        self.geometry(f'{width}x{height}')

    def __center(self) -> None:
        """Places the window in the center of the screen."""

        self.eval(f'tk::PlaceWindow {self.winfo_toplevel()} center')

    def render(self) -> None:
        """Displays the window."""

        self.mainloop()

class Heading(tk.Frame):
    """Represents a heading."""

    def __init__(self, parent: Any, text: str, fg: str = ..., font: tuple = ..., *args: tuple, **kwargs: dict) -> None:
        """
        Configures the heading.
        :param parent: The parent widget containing the heading
        :param text: The heading text
        :param fg: The foreground/text color of the heading
        :param font: The font of the heading
        :param args: Additional arguments
        :param kwargs: Additional keyword arguments
        """

        super().__init__(parent, *args, **kwargs)
        self.grid(row=0, column=0, columnspan=2)
        self.pack_propagate(False)
        self.__init_heading_content(text, fg=fg, font=font, **kwargs)

    def __init_heading_content(self, text: str, fg: str = ..., font: tuple = ..., **kwargs: dict) -> None:
        """
        Sets the heading content.
        :param text: The heading text
        :param fg: The foreground/text color of the heading
        :param font: The font of the heading
        :param kwargs: Additional keyword arguments
        """

        tk.Label(self, text=text, bg=kwargs['bg'], fg=fg, font=font).pack(anchor=tk.CENTER, padx=PADDING, pady=(PADDING, 0))

class Log(tk.Frame):
    """Represents an input log."""

    def __init__(self, parent: Any, fg: str = ..., *args: tuple, **kwargs: dict) -> None:
        """
        Configures the log.
        :param parent: The parent widget containing the log
        :param fg: The foreground color of the log
        :param args: Additional arguments
        :param kwargs: Additional keyword arguments
        """

        super().__init__(parent, *args, **kwargs)
        self.logger = Logger(LOG_FILENAME)
        self.grid(row=1, column=0)
        self.pack_propagate(False)
        self.__init_log_content(fg=fg, **kwargs)
    
    def __init_log_content(self, fg: str = ..., **kwargs: dict) -> None:
        """
        Sets the log content.
        :param fg: The foreground color of the log
        :param kwargs: Additional keyword arguments
        """

        bg = kwargs['bg']
        log_frame = tk.Frame(self, bg=bg)
        # List box
        list_frame = tk.Frame(log_frame, bg=bg)
        tk.Label(list_frame, text='Log', bg=bg, fg=fg, font=(SECONDARY_FONT, SUBHEADING_FONT_SIZE)).pack(side=tk.TOP)
        list_scrollbar = tk.Scrollbar(list_frame, orient=tk.VERTICAL)
        self.log_list = tk.Listbox(list_frame, yscrollcommand=list_scrollbar.set, font=(SECONDARY_FONT, TEXT_FONT_SIZE))
        list_scrollbar.config(command=self.log_list.yview)
        list_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.log_list.pack(expand=True, fill=tk.BOTH)
        for log in self.logger.get_logs():
            self.log_list.insert(tk.END, log)
        list_frame.pack(expand=True, fill=tk.BOTH)
        # Clear list button
        tk.Button(log_frame, text='Clear', command=self.__clear, bg=fg).pack(pady=(PADDING, 0))
        log_frame.pack(expand=True, fill=tk.BOTH)

    def add(self, message: str) -> None:
        """Adds a message to the log."""
        
        if self.logger.log_if_not_exists(message):
            self.log_list.insert(tk.END, message)

    def __clear(self) -> None:
        """Clears the log."""

        self.log_list.delete(0, tk.END)
        self.logger.clear()

class Generator(tk.Frame):
    """Represents a password generator"""

    def __init__(self, parent: Any, log_callback: Callable, fg: str = ..., *args: tuple, **kwargs: dict) -> None:
        """
        Configures the generator.
        :param parent: The parent widget containing the generator
        :param log_callback: The function used to log input
        :param fg: The foreground color of the generator
        :param args: Additional arguments
        :param kwargs: Additional keyword arguments
        """

        super().__init__(parent, *args, **kwargs)
        self.grid(row=1, column=1)
        self.pack_propagate(False)
        self.__init_generator_content(log_callback, fg=fg, **kwargs)

    def __init_generator_content(self, log_callback: Callable, fg: str = ..., **kwargs: dict) -> None:
        """
        Sets the generator content.
        :param fg: The foreground color of the generator
        :param args: Additional arguments
        :param kwargs: Additional keyword arguments
        """

        bg = kwargs['bg']
        # Generate frame
        generate_frame = tk.Frame(self, bg=bg)
        tk.Label(generate_frame, text='Generate', bg=bg, fg=fg, font=(SECONDARY_FONT, SUBHEADING_FONT_SIZE)).pack(side=tk.TOP)
        # Input fields
        input_frame = tk.Frame(generate_frame, bg=bg)
        label_frame = tk.Frame(input_frame, bg=bg)
        tk.Label(label_frame, text='Service', bg=bg, fg=fg, font=(SECONDARY_FONT, TEXT_FONT_SIZE)).pack(anchor=tk.E)
        tk.Label(label_frame, text='Secret', bg=bg, fg=fg, font=(SECONDARY_FONT, TEXT_FONT_SIZE)).pack(anchor=tk.E)
        tk.Label(label_frame, text='Iteration', bg=bg, fg=fg, font=(SECONDARY_FONT, TEXT_FONT_SIZE)).pack(anchor=tk.E)
        tk.Label(label_frame, text='Minimum length', bg=bg, fg=fg, font=(SECONDARY_FONT, TEXT_FONT_SIZE)).pack(anchor=tk.E)
        label_frame.pack(side=tk.LEFT)
        entry_frame = tk.Frame(input_frame, bg=bg)
        self.service = tk.Entry(entry_frame, width=15, bg='white')
        self.service.pack(anchor=tk.W)
        self.secret = tk.Entry(entry_frame, width=15, bg='white')
        self.secret.pack(anchor=tk.W)
        self.iteration = tk.Spinbox(entry_frame, from_=1, to=maxsize, width=TEXT_FONT_SIZE, bg='white')
        self.iteration.pack(anchor=tk.W)
        self.min_length = tk.Spinbox(entry_frame, from_=1, to=maxsize, width=TEXT_FONT_SIZE, bg='white')
        self.min_length.pack(anchor=tk.W)
        entry_frame.pack(side=tk.RIGHT)
        input_frame.pack(side=tk.TOP)
        # Options
        options_frame = tk.Frame(generate_frame, bg=bg)
        self.upper = tk.BooleanVar()
        self.lower = tk.BooleanVar()
        self.number = tk.BooleanVar()
        self.special = tk.BooleanVar()
        self.upper_checkbox = tk.Checkbutton(options_frame, text='uppercase', variable=self.upper, bg=bg, fg=fg, font=(SECONDARY_FONT, TEXT_FONT_SIZE))
        self.upper_checkbox.grid(row=0, column=0, sticky=tk.W)
        self.lower_checkbox = tk.Checkbutton(options_frame, text='lowercase', variable=self.lower, bg=bg, fg=fg, font=(SECONDARY_FONT, TEXT_FONT_SIZE))
        self.lower_checkbox.grid(row=0, column=1, sticky=tk.W)
        self.number_checkbox = tk.Checkbutton(options_frame, text='numbers', variable=self.number, bg=bg, fg=fg, font=(SECONDARY_FONT, TEXT_FONT_SIZE))
        self.number_checkbox.grid(row=1, column=0, sticky=tk.W)
        self.special_checkbox = tk.Checkbutton(options_frame, text='specials', variable=self.special, bg=bg, fg=fg, font=(SECONDARY_FONT, TEXT_FONT_SIZE))
        self.special_checkbox.grid(row=1, column=1, sticky=tk.W)
        options_frame.pack(anchor=tk.S)
        # Generate password button
        def handle_generation() -> None:
            self.input = None
            self.__generate()
            if self.input:
                self.__log_input(log_callback)
        tk.Button(generate_frame, text='Show password', command=handle_generation, bg=fg).pack(pady=PADDING)
        # Display password
        password_frame = tk.Frame(generate_frame, bg=bg)
        password_scrollbar = tk.Scrollbar(password_frame, orient=tk.VERTICAL)
        self.password_text = tk.Text(password_frame, yscrollcommand=password_scrollbar.set, font=(SECONDARY_FONT, TEXT_FONT_SIZE))
        password_scrollbar.config(command=self.password_text.yview)
        password_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.password_text.pack()
        password_frame.pack()
        generate_frame.pack(expand=True, fill=tk.BOTH)

    def __generate(self) -> None:
        """Generates a password."""

        service = self.service.get()
        secret = self.secret.get()
        iteration = self.iteration.get()
        seed = ''.join([service, secret, str(iteration)])
        PasswordGenerator.seed(seed)
        min_length = int(self.min_length.get())
        upper = self.upper.get()
        lower = self.lower.get()
        number = self.number.get()
        special = self.special.get()
        try:
            password = PasswordGenerator.generate(min_length, upper, lower, number, special)
        except ValueError as e:
            password = e
        else:
            options = ''.join(['-',
                ('u' if upper else ''),
                ('l' if lower else ''),
                ('n' if number else ''),
                ('s' if special else '')])
            self.input = ' '.join([service, secret, str(iteration), str(min_length), options])
        finally:
            self.password_text.delete(1.0, tk.END)
            self.password_text.insert(tk.END, password)
    
    def __log_input(self, log_callback: Callable) -> None:
        """Logs input to a log callback function."""

        log_callback(self.input)
