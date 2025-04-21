import random
import time
import os

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
	#global matrix, items, score
	matrix = [["." for _ in range(SIZE)] for _ in range(SIZE)]
	items = []
	score = 0
	
	#random_items(matrix, items)
	#random_items(matrix, items)
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

def clear(): # for thonny
	print("\n" * 32)
	
def view(matrix, score):
	clear()
	print("SCORE:", score)
	matrix = item_indexer(matrix, items)

	for widtht in range(SIZE):
		for lenght in range(len(matrix)):
			print(matrix[widtht][lenght], end=" ")
		print("")

def lisener(matrix, items, score):
	global SIZE
	while True:
		#try:
		comand_input = input("2048py > ")
		
		# Разбиваем команду на части
		parts = comand_input.split()

		if len(parts) == 0:
			print("null")
			continue  # Перезапускаем ввод

		if parts[0] == "/new" and len(parts) == 1:
			random_seed(-1)
			matrix, items, score = generation(SIZE)
			#view(matrix, score)
			#return matrix, items, score
			
		elif parts[0] == "/help" and len(parts) == 1:
			print("/new/help/draw/print/size/seed")
			continue

		elif parts[0] == "/draw" and len(parts) == 1:
			view(matrix, score)
			continue

		elif parts[0] == "/print" and len(parts) > 1:
			print_input = parts[1]
			print(globals()[print_input])
			continue

		elif parts[0] == "/size" and len(parts) > 1:
			size_input = int(parts[1])
			SIZE = size_input
			matrix, items, score = generation(SIZE)
			#continu
				
		elif parts[0] == "/seed" and len(parts) > 1:
			seed_input = parts[1]  # Преобразуем второй элемент в целое число
			seed_input = sum(ord(c) for c in seed_input)
			random_seed(seed_input)  # Вызываем random_seed с этим значением
			matrix, items, score = generation(SIZE)

		elif parts[0] in ["a", "w", "s", "d"] and len(parts) == 1:
			return parts[0]
		else:
			print("ERROR")
			continue

			#return comand_input
		#except Exception as e:
			print(f"Произошла ошибка: {e}. Попробуйте снова.")
			continue 

def movement(matrix, items, score):
	moved = True
	n=0

	MOVE_TO = lisener(matrix, items, score)

	dirs = {
		"a": (0, -1, lambda i: i[0], False),
		"d": (0, 1,  lambda i: i[0], True),
		"w": (1, -1, lambda i: i[1], False),
		"s": (1, 1,  lambda i: i[1], True)
	}

	#if MOVE_TO not in dirs:
		#return

	axis, delta, key_fn, reverse = dirs[MOVE_TO]
	
	# Сортируем индексы по направлению движения
	sorted_ids = sorted(range(len(items)), key=lambda i: key_fn(items[i]), reverse=reverse)
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
					#print(score)
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
			
			#view(matrix, score)
			
			if not blocked:
				matrix[y][x] = "."
				obj[axis] += delta
			
			# Границы
			obj[0] = max(0, min(obj[0], SIZE - 1))
			obj[1] = max(0, min(obj[1], SIZE - 1))

			if obj[axis] != old_pos:
				moved = True
	return score

matrix, items, score= generation(SIZE)
lisener(matrix, items, score)

while True:
	random_items(matrix, items)
	view(matrix, score)
	score = movement(matrix, items, score)
	

