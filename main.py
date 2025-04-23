import random
import os
import sys

if os.name == 'nt':  # Windows
    import msvcrt
else:  # Unix-like systems
    import tty
    import termios

SIZE = 4
VOID_CHAR = "-"
CHAR_SET = [
    "A", "B", "C",
    "D", "E", "F",
    "G", "H", "I",
    "J", "K", "L",
    "M", "N", "O",
    "P"]

def get_generation(SIZE):
	matrix = [[VOID_CHAR for _ in range(SIZE)] for _ in range(SIZE)]
	items = []
	score = 0
	return matrix, items, score

def get_free_positions(matrix, items):
	matrix = get_item_indexer(matrix, items)
    #Cписок всех свободных позиций на карте
	free_positions = []

	for y in range(SIZE):
		for x in range(SIZE):
			if matrix[y][x] == VOID_CHAR:
				free_positions += [[x, y]]
	return free_positions

def get_random_items(matrix, items):
	free_positions = get_free_positions(matrix, items)
	if free_positions:
		x, y = random.choice(free_positions)
		random_char_set = 0 if random.randint(0, 9) < 9 else 1
		items += [[x, y, random_char_set]]
		return items

def get_item_indexer(matrix, items):
	for items_id in range(len(items)):
		matrix[items[items_id][1]][items[items_id][0]] =  CHAR_SET[items[items_id][2]]
	return matrix

def get_view(matrix, score):
	if os.name == 'nt':
		os.system("cls")
	else:
		os.system("clear")
	print("SCORE:", score)
	matrix = get_item_indexer(matrix, items)

	for widtht in range(SIZE):
		for lenght in range(len(matrix)):
			print(matrix[widtht][lenght], end=" ")
		print("")

def get_lisener():
	if os.name == 'nt':  # Windowsd
		while True:
			ch = msvcrt.getch().decode('utf-8')
			if ch in "wasd":
				return ch
			elif ch == "q":
				sys.exit()
	else:  # Unix
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

def process_movement(matrix, items, direction, score):
	moved = True
	old_obj, new_obj = [], []

	DIRS = {
	"a": (0, -1, lambda i: i[0], False),
	"d": (0, 1,  lambda i: i[0], True),
	"w": (1, -1, lambda i: i[1], False),
 	"s": (1, 1,  lambda i: i[1], True)
	}

	axis, delta, key_fn, reverse = DIRS[direction]
	sorted_items = sorted(items, key=key_fn, reverse=reverse)

	while moved:
		moved = False

		for obj in sorted_items[:]:  # копия списка
			x = obj[0]
			y = obj[1]
			matrix[y][x] = VOID_CHAR

			# Удаление дубликатов по позиции и символу
			for other in sorted_items[::-1]:  # с конца
				if other is not obj and obj[0] == other[0] and obj[1] == other[1] and obj[2] == other[2]:
					score += (obj[2]+1)*2
					obj[2] += 1
					items.remove(other)

			# Проверка блокировки
			blocked = any(
				obj[1 - axis] == other[1 - axis] and
				obj[axis] + delta == other[axis] and
				obj[2] != other[2]
				for other in items)

			old_pos = obj[axis]
			old_obj += [obj]

			if not blocked:
				matrix[y][x] = VOID_CHAR
				obj[axis] += delta

			# Walls
			obj[0] = max(0, min(obj[0], SIZE - 1))
			obj[1] = max(0, min(obj[1], SIZE - 1))

			if obj[axis] != old_pos:
				moved = True
			else:
				new_obj += [obj]

	if old_obj != new_obj:
		get_random_items(matrix, items)
	return score

if __name__ == "__main__":
	matrix, items, score = get_generation(SIZE)
	get_random_items(matrix, items)
	get_random_items(matrix, items)

	while True:
		get_view(matrix, score)
		direction = get_lisener()
		score = process_movement(matrix, items, direction, score)
