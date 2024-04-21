#!/usr/bin/env python
# coding: utf-8

# In[ ]:

from multiprocessing import Process, Array

def calculate_element(i, j, matrix1, matrix2, result, rows):
    # Подсчёт элементов в матрице-результате
    res = 0
    for k in range(rows):
        res += matrix1[i][k] * matrix2[k][j]
    result[i * len(matrix2[0]) + j] = res

def multiply_matrices(matrix1, matrix2, result, num_processes):
    # Умножение матриц с мультипроцессорными вычислениями
    rows = len(matrix1)
    cols = len(matrix2[0])

    processes = []
    for i in range(rows):
        for j in range(cols):
            process = Process(target=calculate_element, args=(i, j, matrix1, matrix2, result, len(matrix2)))
            processes.append(process)
            process.start()

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
    # Чтение матриц из файлов
    matrix1 = read_matrix_from_file("matrix1.txt")
    matrix2 = read_matrix_from_file("matrix2.txt")

    # Создание результирующей матрицы
    result = Array('i', [0] * len(matrix1) * len(matrix2[0]))

    # Процесс умножения
    num_processes = 4  # Тут можно менять по своему желанию
    multiply_matrices(matrix1, matrix2, result, num_processes)

    # Преобразование результата в матрицу
    result_matrix = [[result[i * len(matrix2[0]) + j] for j in range(len(matrix2[0]))] for i in range(len(matrix1))]

    # Запись матрицы результата в файл
    write_matrix_to_file(result_matrix, "result_matrix.txt")
