import numpy as np

def game_core_v2(number):
    '''Определяем середину между минимумом и максимумом, далее - сравнием с загаданным числом.
       В зависимости от результата сравнения, изменяем границы поиска.
       Функция принимает загаданное число и возвращает число попыток'''
    count = 1
    maximum = 101
    minimum = 0
    predict = (minimum+maximum)//2
    while predict != number:
        count += 1
        if number > predict:
            minimum = predict
        else:
            maximum = predict
        predict = (minimum+maximum)//2
    return(count)
        
        
def score_game(game_core):
    '''Запускаем игру 1000 раз, чтобы узнать, как быстро игра угадывает число'''
    count_ls = []
    np.random.seed(1)  # фиксируем RANDOM SEED, чтобы ваш эксперимент был воспроизводим!
    random_array = np.random.randint(1,101, size=(1000))
    for number in random_array:
        count_ls.append(game_core_v2(number))
    score = int(np.mean(count_ls))
    print(f"Ваш алгоритм угадывает число в среднем за {score} попыток")
    return(score)

score_game(game_core_v2)