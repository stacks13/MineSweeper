from tkinter import *
import random as rd
import time
from tkinter import messagebox


w, h, m = 16, 16, 40
mine_at_first = False

window = Tk()

press = 0
start_time = time.time()



class Mines:
	mines = []
	not_mines = []
	mine_buttons = [[0 for x in range(w+1)] for y in range(h+1)]
	mine_label = None
	time_label = None
	state = False

	@staticmethod
	def disable_buttons():
		for x in range(1, len(Mines.mine_buttons)):
			for y in range(1, len(Mines.mine_buttons[x])):
				Mines.mine_buttons[x][y].config(state=DISABLED)

	@staticmethod
	def clear_all():
		Mines.not_mines.clear()
		Mines.mines.clear()
		for x in range(1, len(Mines.mine_buttons)):
			for y in range(1, len(Mines.mine_buttons[x])):
				Mines.mine_buttons[x][y] = None

def clock():
	if Mines.state:
		Mines.time_label.config(text=round(time.time() - start_time, 1))
		window.after(100, clock)


def start():

	global window
	Mines.clear_all()

	counter = 0
	for child in window.winfo_children():
		counter += 1
		child.destroy()

	for x in range(1,w+1):
		for y in range(1,h+1):
			button = Button(window, text="", width=1, bg='#c1c1c1')
			button.grid(row=x, column=y)
			button.bind("<ButtonPress-1>", button_click)
			button.bind("<ButtonPress-3>", button_rclick)
			Mines.mine_buttons[x][y] = button
			Mines.not_mines.append((x, y))

	mine_label = Label(window, text=m)
	mine_label.grid(row=w+2, column=int((h+1)/2), columnspan=2)

	time_label = Label(window, text="Start")
	time_label.grid(row=w+3, column=int((h+1)/2), columnspan=2)

	Mines.mine_label = mine_label
	Mines.time_label = time_label

	if mine_at_first:
		plant_mines()

	window.mainloop()


def except_mine(n, end, start = 1):
	return list(range(start, n)) + list(range(n+1, end))


def plant_mines(row=None, col=None):
	count = 1
	tots = []
	for x in range(1, w+1):
		for y in range(1, h+1):
			if x != row or y != col:
				tots.append((x,y))

	while count<=m:

		print(len(tots))
		rand_cell = rd.choice(tots)

		if not check_mine(rand_cell[0], rand_cell[1]):
			Mines.mines.append((rand_cell[0], rand_cell[1]))
			Mines.not_mines.remove((rand_cell[0], rand_cell[1]))
			tots.remove(rand_cell)
			count+=1


def button_click(event):
	if event.widget['state'] != DISABLED:
		global start_time, press

		grid_info = event.widget.grid_info()
		curr_row, curr_col = grid_info['row'], grid_info['column']
		
		if press == 0:
			if not mine_at_first:
				plant_mines(curr_row, curr_col)
			start_time = time.time()
			Mines.state=True
			window.after(100, clock)
			press += 1

		if event.widget['text'] == '¶':
			pass
		else:
			reveal(curr_row, curr_col, event.widget, False)


def button_rclick(event):
	if event.widget['state'] != DISABLED:
		if event.widget['text'] == '¶':
			mines_left = int(Mines.mine_label['text'])
			Mines.mine_label.config(text=mines_left+1)
			event.widget.config(text='', bg='#c1c1c1')
		else:
			mines_left = int(Mines.mine_label['text'])
			Mines.mine_label.config(text=mines_left - 1)
			event.widget.config(text='¶', bg='#f7b071')
		

def reveal(x, y, widget, from_zero=True):
	global window

	if check_mine(x, y) and not from_zero:
		global press
		Mines.state=False
		press = 0
		print("Game Over")
		Mines.disable_buttons()
		widget.configure(bg='red')
		
		ask = messagebox.askokcancel('Game Over', 'You lose. Retry?')
		if ask:
			start()

	else:
		no = get_no(x, y)

		if no==0:
			widget.config(state=DISABLED)
			widget.config(bg=window.cget('bg'))
		else:
			widget.config(text=str(no), bg='#c7d5ed')

		if Mines.not_mines.count((x, y)) != 0:
			Mines.not_mines.remove((x, y))

		if len(Mines.not_mines) == 0:
			celebrate()

		if no == 0:
			if find_in_grid(x-1, y-1) and (not check_reveal(x-1, y-1)) :
				reveal(x-1, y-1, find_in_grid(x-1, y-1))
			if find_in_grid(x-1, y) and (not check_reveal(x-1, y)):
				reveal(x-1, y, find_in_grid(x-1, y))
			if find_in_grid(x-1, y+1) and (not check_reveal(x-1, y+1)) :
				reveal(x-1, y+1, find_in_grid(x-1, y+1))
			if find_in_grid(x, y-1) and (not check_reveal(x, y-1))  :
				reveal(x, y-1, find_in_grid(x, y-1))
			if find_in_grid(x, y+1) and (not check_reveal(x, y+1))  :
				reveal(x, y+1, find_in_grid(x, y+1))
			if find_in_grid(x+1, y-1) and (not check_reveal(x+1, y-1))  :
				reveal(x+1, y-1, find_in_grid(x+1, y-1))
			if find_in_grid(x+1, y) and (not check_reveal(x+1, y))  :
				reveal(x+1, y, find_in_grid(x+1, y))
			if find_in_grid(x+1, y+1) and (not check_reveal(x+1, y+1))  :
				reveal(x+1, y+1, find_in_grid(x+1, y+1))


def check_mine(x, y):

	for z in range(len(Mines.mines)):
		if (Mines.mines[z])[0] == x and (Mines.mines[z])[1] == y:
			return True
	return False


def celebrate():
	print("YOU WIN")
	Mines.disable_buttons()
	end_time = time.time()
	Mines.state=False
	global press
	press = 0

	ask = messagebox.askokcancel('Congratulations', 'You won in ' + str(round(end_time - start_time, 1)) + ' seconds. Wanna go again?')

	if ask:
		start()
	return


def find_in_grid(x, y):

	try:
		widget = Mines.mine_buttons[x][y]
		return widget
	except Exception:
		return None


# true if the tile is revealed and false otherwise
def check_reveal(x, y):
	if Mines.not_mines.count((x, y)) == 0:
		return True
	return False


def get_no(x, y):
	no = 0
	if check_mine(x + 1, y):
		no += 1
	if check_mine(x - 1, y):
		no += 1
	if check_mine(x, y + 1):
		no += 1
	if check_mine(x, y - 1):
		no += 1
	if check_mine(x + 1, y + 1):
		no += 1
	if check_mine(x + 1, y - 1):
		no += 1
	if check_mine(x - 1, y + 1):
		no += 1
	if check_mine(x - 1, y - 1):
		no += 1
	return no

if __name__ == '__main__':
	start()

