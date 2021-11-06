from tkinter import *   
import game_grabber as gg
import sys
import webbrowser
 
root = Tk()
root.title("BotScan")
root.geometry("290x400")


user_label = Label(root, text = "Username:")
user_label.grid(column = 0, row = 1)
user_text = StringVar()
user_entry = Entry(root, textvariable = user_text, bg = "gray90")
user_entry.grid(column = 1, row = 1)


variant_label = Label(root, text = "Variant:")
variant_label.grid(column = 0, row = 2)
variant_text = StringVar()
variant_entry = Entry(root, textvariable = variant_text, bg = "gray90")
variant_entry.grid(column = 1, row = 2)

speed_label = Label(root, text = "Speed:")
speed_label.grid(column = 0, row = 3)
speed_text = StringVar()
speed_entry = Entry(root, textvariable = speed_text, bg = "gray90")
speed_entry.grid(column = 1, row = 3)

rating_label = Label(root, text = "Min Rating:")
rating_label.grid(column = 0, row = 4)
rating_text = StringVar()
rating_entry = Entry(root, textvariable = rating_text, bg = "gray90")
rating_entry.grid(column = 1, row = 4)

msg = Label(root, text = "Patience")
msg.grid(column = 1, row = 5)

links = Listbox(root, bg = "gray90", fg = "RoyalBlue")
links.grid(column = 1,row = 6)
scrollbar = Scrollbar(root)
scrollbar.grid(column = 2, row = 6)
links.config(yscrollcommand = scrollbar.set)
scrollbar.config(command = links.yview)

exit_btn = Button(root, text = "Exit", fg = "red", command = sys.exit)
exit_btn.grid(column = 0, row = 6, sticky = N)


def submit():
    try:
        data = gg.scan(user_text.get(), variant_text.get(), speed_text.get(), rating_text.get())
        links.delete(0, links.size())
        for x in range(0, len(data[0])):
            links.insert(END, f"{x+1}. {data[0][x]}, {round(data[1][x], 3)}")
        msg.config(text = "Done!", fg = "green")
    except:
        msg.config(text = "Error", fg = "red")


submit_btn = Button(root, text = "Submit", fg = "green", command = submit)
submit_btn.grid(column = 0, row = 5)

def lichess_it():
    try: 
        stuff = links.get(links.curselection()).replace(",", "")
        game = stuff.split()[1]
        webbrowser.open_new(f"https://lichess.org/{game}")
    except:
        pass


link_btn = Button(root, text = "Open", fg = "green", command = lichess_it)
link_btn.grid(column = 1, row = 7)

def help():
    help_root = Tk()
    help_root.title("Help with BotScan")
    help_root.geometry("450x450")
    help_text = Message(help_root, justify = LEFT, width = 400)
    help_text.pack()
    f = open("botscan_help.txt")
    words = f.read()
    help_text.config(text = words)


help_btn = Button(root, text = "Help", fg = "orange", command = help)
help_btn.grid(column = 0, row = 0)

root.mainloop()
