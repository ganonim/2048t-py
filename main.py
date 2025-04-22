import random
import time
import os
import sys
import tty
import termios

SIZE = 4
char_set = [
    "0", "1", "2",
	"3", "4", "5",
	"6", "7", "8",
	"9", "A", "B",
	"C", "D", "E",
	"F"
	]

def generation(SIZE):
	matrix = [["." for _ in range(SIZE)] for _ in range(SIZE)]
	items = []
	score = 0

	return matrix, items, score

def get_free_positions(matrix, items):
	matrix = item_indexer(matrix, items)
    #Cписок всех свободных позиций на карте
	free_positions = []

	for y in range(SIZE):
		for x in range(SIZE):
			if matrix[y][x] == ".":
				free_positions += [[x, y]]
	return free_positions

def random_items(matrix, items):
	free_positions = get_free_positions(matrix, items)
	if free_positions:
		x, y = random.choice(free_positions)
		#random_char_sett = random.randint(0, 1)
		items += [[x, y, 0 ]]
		return items


def random_seed(seed):
	if seed == -1:
		new_seed = random.randint(10**(8-1), 10**8 - 1)
		random.seed(new_seed)
	else:
		random.seed(seed)

def item_indexer(matrix, items):
	for items_id in range(len(items)):
		matrix[items[items_id][1]][items[items_id][0]] =  char_set[items[items_id][2]]
	return matrix

def view(matrix, score):
	os.system("clear")
	print("SCORE:", score)
	matrix = item_indexer(matrix, items)

	for widtht in range(SIZE):
		for lenght in range(len(matrix)):
			print(matrix[widtht][lenght], end=" ")
		print("")

def lisener():
	fd = sys.stdin.fileno()
	old_settings = termios.tcgetattr(fd)
	try:
		tty.setraw(fd)
		while True:
			ch = sys.stdin.read(1)
			if ch in "wasd":
				return ch
			elif ch == "q":
				sys.exit()
	finally:
		termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)  # Восстанавливаем настройки терминала

def movement(matrix, items, score):
	moved = True
	n=0
	old_obj, new_obj = [], []

	MOVE_TO = lisener()

	dirs = {
		"a": (0, -1, lambda i: i[0], False),
		"d": (0, 1,  lambda i: i[0], True),
		"w": (1, -1, lambda i: i[1], False),
		"s": (1, 1,  lambda i: i[1], True)
	}

	axis, delta, key_fn, reverse = dirs[MOVE_TO]

	# Сортируем индексы по направлению движения
	sorted_ids = sorted(range(len(items)), key=lambda i: key_fn(items[i]), reverse=reverse)
	old_items = []

	while moved:
		moved = False

		for obj in items[:]:  # копия списка
			x = obj[0]
			y = obj[1]
			symbol = obj[2]
			matrix[y][x] = "."

			# Удаление дубликатов по позиции и символу
			for other in items[::-1]:  # с конца
				if other is not obj and obj[0] == other[0] and obj[1] == other[1] and obj[2] == other[2]:
					score += (obj[2]+1)*2
					obj[2] += 1
					items.remove(other)

			# Проверка блокировки
			blocked = any(
				obj[1 - axis] == other[1 - axis] and
				obj[axis] + delta == other[axis] and
				obj[2] != other[2]
				for other in items
			)

			old_pos = obj[axis]
			old_obj += [obj]

			if not blocked:
				matrix[y][x] = "."
				obj[axis] += delta

			# Границы
			obj[0] = max(0, min(obj[0], SIZE - 1))
			obj[1] = max(0, min(obj[1], SIZE - 1))
			if obj[axis] != old_pos:
				moved = True
			else:
				new_obj += [obj]

	if old_obj != new_obj:
		random_items(matrix, items)
	return score

matrix, items, score= generation(SIZE)
random_items(matrix, items)
random_items(matrix, items)

while True:
	view(matrix, score)
	score = movement(matrix, items, score)
