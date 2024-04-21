#!/usr/bin/env python
# coding: utf-8

# In[ ]:

from multiprocessing import Process, Array, Event
import random

def generate_matrix(size):
    return [[random.randint(1, 10) for _ in range(size)] for _ in range(size)]

def calculate_element(i, j, matrix1, matrix2, result, rows, stop_event):
    # Подсчёт элементов в матрице-результате
    res = 0
    for k in range(rows):
        if stop_event.is_set():
            return
        res += matrix1[i][k] * matrix2[k][j]
    result[i * len(matrix2[0]) + j] = res

def multiply_matrices(matrix1, matrix2, result, stop_event, num_processes):
    # Умножение матриц с мультипроцессорными вычислениями
    rows = len(matrix1)
    cols = len(matrix2[0])

    processes = []
    for i in range(rows):
        for j in range(cols):
            process = Process(target=calculate_element, args=(i, j, matrix1, matrix2, result, len(matrix2), stop_event))
            processes.append(process)
            process.start()
            if len(processes) >= num_processes:
                for p in processes:
                    p.join()
                    if stop_event.is_set():
                        return
                processes = []

    for process in processes:
        process.join()

def read_matrix_from_file(filename):
    with open(filename, 'r') as file:
        matrix = [[int(x) for x in line.split()] for line in file]
    return matrix

def write_matrix_to_file(matrix, filename):
    with open(filename, 'w') as file:
        for row in matrix:
            file.write(' '.join(map(str, row)) + '\n')

if __name__ == "__main__":
    # Генерация случайных квадратных матриц заданной размерности
    matrix_size = 2  # Размерность матриц
    matrix1 = generate_matrix(matrix_size)
    matrix2 = generate_matrix(matrix_size)

    # Создание результирующей матрицы
    result = Array('i', [0] * matrix_size * matrix_size)

    # Создание события для остановки процесса перемножения
    stop_event = Event()

    # Процесс умножения
    num_processes = 4  # Тут можно менять по своему желанию
    multiply_process = Process(target=multiply_matrices, args=(matrix1, matrix2, result, stop_event, num_processes))
    multiply_process.start()

    # Задержка перед остановкой процесса (в данном случае 5 секунд)
    import time
    time.sleep(5)

    # Установка события остановки процесса
    stop_event.set()
    multiply_process.join()

    # Преобразование результата в матрицу
    result_matrix = [[result[i * matrix_size + j] for j in range(matrix_size)] for i in range(matrix_size)]

    print("Matrix 1:")
    for row in matrix1:
        print(row)
    
    print("\nMatrix 2:")
    for row in matrix2:
        print(row)
    

    # Запись матрицы результата в файл
    write_matrix_to_file(result_matrix, "result_matrix_evil.txt")
