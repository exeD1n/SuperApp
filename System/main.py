# main.py
from ttkthemes import ThemedTk
from app import App

if __name__ == "__main__":
    root = ThemedTk(theme="arc")
    app = App(root)
    root.mainloop()