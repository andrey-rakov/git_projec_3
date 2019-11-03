import os
import pygame
import random


# основные константы
FPS = 30
number_round = 1 # номер заезда
number_points = 0 # количество набранных очков
points_to_win = 200 # количество очков которые надо набрать для победы
n = 8 # размерность поля (квадрат nхn)
# основные цвета
white = (255, 255, 255)
black = (0, 0, 0)
gray_1 = (210, 210, 210)
gray_2 = (240, 240, 240)
blue = (0, 0, 255)
red = (255, 0, 0)
green = (0, 255, 0)
# подгружаемые рисунки
imag_0 = pygame.image.load(os.path.join('data', '0.jpg'))
imag_1 = pygame.image.load(os.path.join('data', '1.jpg'))
imag_bot_0 = pygame.image.load(os.path.join('data', 'bot_0.jpg'))
imag_bot_1 = pygame.image.load(os.path.join('data', 'bot_1.jpg'))
imag_bot_2 = pygame.image.load(os.path.join('data', 'bot_2.jpg'))
imag_bot_3 = pygame.image.load(os.path.join('data', 'bot_3.jpg'))
# создание окна игры и основы для интерфейса
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((940, 740))
pygame.display.set_caption("Игра - КодеБот (лайт версия)")
screen.fill(gray_1)
pygame.draw.rect(screen, black, (5, 5, 930, 80), 1)
pygame.draw.rect(screen, black, (655, 84, 280, 651), 1)
pygame.draw.rect(screen, black, (5, 5, 930, 730), 1)
font_1 = pygame.font.SysFont('mistral', 60)
text_1 = font_1.render('КодеБот', 1, blue)
screen.blit(text_1, (40, 15))
font_2 = pygame.font.SysFont('Monotype Corsiva', 20)
text_2 = font_2.render('Дорогой друг! Помоги роботу КодеБоту добраться до цели.', 1, white)
screen.blit(text_2, (250, 20))
text_3 = font_2.render('Программируй его движения стрелками на клавиатуре или кнопками на экране.', 1, white)
screen.blit(text_3, (250, 50))


class Game():
    def __init__(self):
        self.ind = [0, 1, 0, -1] # вспомогательный список
        self.start_motion = False  # определение начала движения робота
        self.end_round = False  # определение завершения текущего заезда
        self.route = [] # текущий список с командами для робота
        self.number_points = 0 # количество очков в текущем заезде
        self.number_attempts = 0  # количество попыток прохождения текущего заезда, используется для подсчёта баллов
        self.number_errors = 0  # количество ошибок при движении робота, используется для подсчёта баллов
        self.number_wrong_answers = 0  # количество неправильно выбранных ответов, используется для подсчёта баллов
        self.number_passed_cells = 0  # колличество пройденных клеток поля
        self.text_example = '' # переменная в которой будет хранится текст примера
        self.tek_i = 0 # номер строки для вычисления перемещения робота
        self.tek_j = 0 # номер столбца для вычисления перемещения робота
        self.answer = 0 # правильный ответ на текущий пример
        self.a_variable = 90 # ограничения для генерации примера
        self.b_variable = 90
        self.c_variable = 90
        self.d_variable = 90
        self.f_from_variable = 25
        self.f_before_variable = 500
        self.orientation = 0 # ориентация робота, возможные значения 0, 1, 2, 3
        self.matrix = self.random_matrix() # генерируем случайную матрицу (лабиринт)
        self.drawing_labyrinth() # рисуем сгенерированный лабиринт
        self.list_end_cells = self.end_cells() # список коненцевых ячеек лабиринта
        self.long = len(self.list_end_cells)
        self.list_answers = self.cells_with_answers() # матрица для пометки концевых ячеек
        self.text_example, self.answer = self.task_generation() # генерируем пример
        self.information_panel() # выводим информационну панель
        self.control_panel() # выводим панель управления
        self.answer_choice = self.wrong_options() # список случайных неправильных ответов
        i = self.draw_answer_choice() # расставляем случайным образом ответы в концевые ячейки
        self.start_i = self.list_end_cells[0][0] # делаем настройки перед стартом заезда
        self.start_j = self.list_end_cells[0][1]
        self.finish_i = self.list_end_cells[i][0]
        self.finish_j = self.list_end_cells[i][1]
        self.orientation = self.robot_on_strat()
        self.orientation_first = self.orientation
        self.orientation_first_new = self.orientation
        self.tek_i, self.tek_j = self.start_i, self.start_j
        self.start_new_i, self.start_new_j = self.start_i, self.start_j
        self.tek_new_i, self.tek_new_j = self.start_i, self.start_j


    # вывод изображения робота на начальную позицию
    def robot_on_strat(self):
        orientation = ''
        try:
            if self.start_j != 0:
                if self.matrix[self.start_i][self.start_j - 1] == 1:
                    orientation = 0
            if self.matrix[self.start_i + 1][self.start_j] == 1:
                orientation = 1
            if self.start_j != n:
                if self.matrix[self.start_i][self.start_j + 1] == 1:
                    orientation = 2
            if orientation == '':
                orientation = 3
        except Exception:
            orientation = 0
        self.draw_bot(self.start_i, self.start_j, self.start_i, self.start_j, orientation)
        return orientation


    # рисование на поле вариантов ответов для примера
    def draw_answer_choice(self):
        ii = random.randint(0, self.long - 2) + 1
        font_0 = pygame.font.Font(os.path.join('data', 'Segoe UI Symbol.ttf'), 20)
        text_0 = font_0.render(str(self.answer), 1, blue)
        screen.blit(text_0, (self.list_end_cells[ii][0] * 80 + 35, self.list_end_cells[ii][1] * 80 + 115))
        for i in range(1, self.long):
            if self.answer_choice[i - 1] != 0:
                text_0 = font_0.render(str(self.answer_choice[i - 1]), 1, blue)
                if i != ii:
                    screen.blit(text_0, (self.list_end_cells[i][0] * 80 + 35, self.list_end_cells[i][1] * 80 + 115))
        return ii


    # генерируем неправильные варианты для конечных ячек лабиринта
    def wrong_options(self):
        k = 0
        answer_choice = []
        while True:
            if random.randint(0, 2) == 1:
                answer_choice.append(self.answer + random.randint(5, 30))
            else:
                answer_choice.append(self.answer - random.randint(5, 30))
            k += 1
            if k == self.long - 1:
                if len(answer_choice) != len(set(answer_choice)):
                    k = 0
                    answer_choice = []
                else:
                    break
        return answer_choice


    # генерация примера для решения
    def task_generation(self):
        while True:
            act1 = random.randint(0, 2)
            act2 = random.randint(0, 2)
            a = random.randint(0, self.a_variable)
            b = random.randint(0, self.b_variable)
            c = random.randint(0, self.c_variable)
            d = random.randint(0, self.d_variable)
            answer = 0
            if act1 == 1 and act2 == 1:
                answer = a * (b + c) + d
                act1_s = '+'
                act2_s = '+'
            elif act1 == 1 and act2 == 2:
                answer = a * (b + c) - d
                act1_s = '+'
                act2_s = '-'
            elif act1 == 2 and act2 == 1:
                answer = a * (b - c) + d
                act1_s = '-'
                act2_s = '+'
            elif act1 == 2 and act2 == 2:
                answer = a * (b - c) - d
                act1_s = '-'
                act2_s = '-'
            if self.f_from_variable <= answer <= self.f_before_variable:
                text_example = '{}{}({} {} {}) {} {}'.format(a, chr(8729), b, act1_s, c, act2_s, d)
                break
        return text_example, answer


    # список на котором отмечены ячейки с вариантами ответов на решение примера
    def cells_with_answers(self):
        list_answers = [[0 for i in range(n)] for j in range(n)]
        for i in range(self.long):
            list_answers[self.list_end_cells[i][0]][self.list_end_cells[i][1]] = 1
        return list_answers


    # находим список конечных ячеек в лабиринте
    def end_cells(self):
        arr = []
        for i in range(n):
            for j in range(n):
                if self.matrix[i][j] == 1:
                    s = 0
                    for q in range(4):
                        if 0 <= i + self.ind[q] < n and 0 <= j + self.ind[3 - q] < n:
                            s += self.matrix[i + self.ind[q]][j + self.ind[3 - q]]
                    if s == 1:
                        arr.append([i, j])
        return arr


    # Вывод информационной панели
    def information_panel(self):
        text = ['Реши пример и выбери путь', 'для движения робота', 'Для запуска программы',
                'нажми клавишу Enter ', 'или кнопку с треугольником.', 'Если сложно сразу ввести',
                'весь код, вводи и ', 'запускай код по частям']
        pygame.draw.rect(screen, white, (660, 90, 270, 380))
        font_1 = pygame.font.SysFont('Times New Roman', 30)
        text_1 = font_1.render('Заезд №: {}'.format(number_round), 1, blue)
        screen.blit(text_1, (725, 95))
        font_2 = pygame.font.SysFont('Times New Roman', 30)
        text_2 = font_2.render(self.text_example, 1, red)
        screen.blit(text_2, (680, 130))
        font_3 = pygame.font.SysFont('Times New Roman', 20)
        text_3 = font_3.render('Количество очков: {}'.format(number_points), 1, blue)
        screen.blit(text_3, (670, 165))
        font_4 = pygame.font.SysFont('Monotype Corsiva', 20)
        for i in range(len(text)):
            if i < 5:
                text_4 = font_4.render(text[i], 1, green)
            else:
                text_4 = font_4.render(text[i], 1, red)
            screen.blit(text_4, (670, 300 + i * 20))


    # Вывод панели управления
    def control_panel(self):
        kod = [63, 8630, 10226, 8593, 9655, 8595, 32, 8631, 10007]
        k = 0
        for i in range(3):
            for j in range(3):
                if (i == 0 and j == 0) or (i == 2 and j == 0):
                    color = (200, 255, 200)
                else:
                    color = (240, 240, 240)
                pygame.draw.rect(screen, color, (665 + i * 85, 475 + j * 85, 85, 85))
                pygame.draw.rect(screen, (100, 100, 100), (665 + i * 85, 475 + j * 85, 85, 85), 2)
                font_symbol = pygame.font.Font(os.path.join('data', 'Segoe UI Symbol.ttf'), 50)
                text_0 = font_symbol.render(chr(kod[k]), 1, blue)
                screen.blit(text_0, (695 + i * 85, 480 + j * 85))
                k += 1


    # Индикация команд программирования робота на панели управления
    def indication_commands(self, orientation):
        indexes = {0: ((1, 0), 8593), 1: ((2, 1), 8631), 2: ((1, 2), 8595),
                   3: ((0, 1), 8630), 4: ((1, 1), 9655), 5: ((0, 2), 10226)}
        font_symbol = pygame.font.Font(os.path.join('data', 'Segoe UI Symbol.ttf'), 50)
        font_symbol_1 = pygame.font.Font(os.path.join('data', 'Segoe UI Symbol.ttf'), 35)
        pygame.draw.rect(screen, (200, 255, 200), (665 + 0 * 85, 475 + 0 * 85, 85, 85))
        pygame.draw.rect(screen, (100, 100, 100), (665 + 0 * 85, 475 + 0 * 85, 85, 85), 2)
        pygame.draw.rect(screen, (200, 255, 200), (665 + 2 * 85, 475 + 0 * 85, 85, 85))
        pygame.draw.rect(screen, (100, 100, 100), (665 + 2 * 85, 475 + 0 * 85, 85, 85), 2)
        if orientation < 6:
            i, j, symbol = *indexes[orientation][0], indexes[orientation][1]
            text_0 = font_symbol.render(chr(symbol), 1, red)
            screen.blit(text_0, (695, 480))
            text_1 = font_symbol.render(chr(symbol), 1, red)
            screen.blit(text_1, (695 + i * 85, 480 + j * 85))
            text_1 = font_symbol_1.render(str(len(self.route)), 1, red)
            screen.blit(text_1, (686 + 2 * 85, 492 + 0 * 85))
            pygame.display.flip()
            text_1 = font_symbol.render(chr(symbol), 1, blue)
            screen.blit(text_1, (695 + i * 85, 480 + j * 85))
            pygame.time.delay(250)
            pygame.display.flip()
        else:
            pass


    # Генерация бинарной матрицы (определяющей вид лабиринта)
    def random_matrix(self):
        matrix = [[0 for i in range(n)] for j in range(n)]
        ind = [0, 1, 0, -1]
        arr = []
        start_i = 0
        start_j = random.randint(1, n) - 1
        matrix[start_i][start_j] = 1
        t = False
        flag = 1
        arr.append([start_i, start_j])
        while not t:
            ii = 0
            while True:
                tek_i, tek_j = arr[ii][0], arr[ii][1]
                k = random.randint(0, 3)
                new_i, new_j = tek_i + ind[k], tek_j + ind[3 - k]
                if 0 <= new_i < n and 0 <= new_j < n and matrix[new_i][new_j] == 0:
                    j = 0
                    for i in range(4):
                        if new_i + ind[i] >= 0 and new_i + ind[i] < n and new_j + ind[3 - i] >= 0 and \
                                (new_j + ind[3 - i] < n and matrix[new_i + ind[i]][new_j + ind[3 - i]] == 1):
                            j += 1
                    if j == 1:
                        matrix[new_i][new_j] = 1
                        if random.randint(0, 4) == random.randint(0, 4):
                            arr.append([new_i, new_j])
                        else:
                            arr[ii][0] = new_i
                            arr[ii][1] = new_j
                flag = flag + 1
                if flag >= 20 * n * n:
                    k = 0
                    for i in range(n - 1):
                        for j in range(n - 1):
                            if sum([matrix[i + ind[q]][j + ind[3 - q]] for q in range(4)]) == 1 and matrix[i][j] == 1:
                                k += 1
                    if k > 4:
                        t = True
                    else:
                        matrix = [[0 for i in range(n)] for j in range(n)]
                        arr = []
                        start_i = 0
                        start_j = random.randint(1, n) - 1
                        matrix[start_i][start_j] = 1
                        t = False
                        flag = 1
                        arr.append([start_i, start_j])
                        ii = 0
                if ii == len(arr) - 1:
                    break
                else:
                    ii += 1
        return matrix


    # рисование поля с лабиринтом
    def drawing_labyrinth(self):
        for j in range(n):
            for i in range(n):
                myRect = (i * 80 + 10, j * 80 + 90, 80, 80)
                if self.matrix[i][j] == 0:
                    screen.blit(imag_0, myRect)
                else:
                    screen.blit(imag_1, myRect)


    # рисование робота
    def draw_bot(self, x0, y0, x1, y1, orientation):
        myRect = (x0 * 80 + 10, y0 * 80 + 90, 80, 80)
        screen.blit(imag_1, myRect)
        myRect = (x1 * 80 + 19, y1 * 80 + 98, 80, 80)
        if orientation == 0:
            imag_bot = imag_bot_0
        elif orientation == 1:
            imag_bot = imag_bot_1
        elif orientation == 2:
            imag_bot = imag_bot_2
        else:
            imag_bot = imag_bot_3
        screen.blit(imag_bot, myRect)


    # индикация ошибки во время движения робота
    def draw_bot_error(self, x0, y0, x1, y1, orientation):
        myRect = (x0 * 80 + 10, y0 * 80 + 90, 80, 80)
        screen.blit(imag_1, myRect)
        pygame.draw.rect(screen, (250, 0, 0), (x0 * 80 + 11, y0 * 80 + 91, 76, 76), 4)
        myRect = (x1 * 80 + 19, y1 * 80 + 98, 80, 80)
        if orientation == 0:
            imag_bot = imag_bot_0
        elif orientation == 1:
            imag_bot = imag_bot_1
        elif orientation == 2:
            imag_bot = imag_bot_2
        else:
            imag_bot = imag_bot_3
        screen.blit(imag_bot, myRect)
        pygame.time.delay(500)
        pygame.display.flip()
        self.draw_bot(x0, y0, x1, y1, orientation)


    # реакция робота на победу в заезде
    def draw_bot_victory(self, x0, y0, x1, y1, orientation):
        for i in range(8):
            orientation += 1
            orientation %= 4
            myRect = (x0 * 80 + 10, y0 * 80 + 90, 80, 80)
            screen.blit(imag_1, myRect)
            pygame.draw.rect(screen, (0, 0, 250), (x0 * 80 + 11, y0 * 80 + 91, 76, 76), 4)
            myRect = (x1 * 80 + 19, y1 * 80 + 98, 80, 80)
            if orientation == 0:
                imag_bot = imag_bot_0
            elif orientation == 1:
                imag_bot = imag_bot_1
            elif orientation == 2:
                imag_bot = imag_bot_2
            else:
                imag_bot = imag_bot_3
            screen.blit(imag_bot, myRect)
            pygame.time.delay(500)
            pygame.display.flip()
            self.draw_bot(x0, y0, x1, y1, orientation)


    # организуем движение робота по полю
    def robot_motion(self):
        self.start_motion = False
        self.number_attempts += 1
        self.tek_i = self.start_new_i
        self.tek_j = self.start_new_j
        self.orientation = self.orientation_first_new
        for i in range(len(self.route)):
            if self.route[i] == 0:
                self.tek_new_i = self.tek_i + self.ind[self.orientation]
                self.tek_new_j = self.tek_j + self.ind[3 - self.orientation]
                if 0 <= self.tek_new_i <= n - 1 and 0 <= self.tek_new_j <= n - 1 and \
                        self.matrix[self.tek_new_i][self.tek_new_j] == 1:
                    self.number_passed_cells += 1
                    self.draw_bot(self.tek_i, self.tek_j, self.tek_new_i, self.tek_new_j, self.orientation)
                    self.tek_i, self.tek_j = self.tek_new_i, self.tek_new_j
                    if self.list_answers[self.tek_i][self.tek_j] == 1:
                        self.number_wrong_answers += 1
                else:
                    self.draw_bot_error(self.tek_i, self.tek_j, self.tek_i, self.tek_j, self.orientation)
                    self.number_errors += 1
            elif self.route[i] == 1:
                self.orientation += 1
                self.orientation %= 4
                self.draw_bot(self.tek_i, self.tek_j, self.tek_i, self.tek_j, self.orientation)
            elif self.route[i] == 2:
                self.tek_new_i = self.tek_i + (-1) * self.ind[self.orientation]
                self.tek_new_j = self.tek_j + (-1) * self.ind[3 - self.orientation]
                if 0 <= self.tek_new_i <= n - 1 and 0 <= self.tek_new_j <= n - 1 and \
                        self.matrix[self.tek_new_i][self.tek_new_j] == 1:
                    self.number_passed_cells += 1
                    self.draw_bot(self.tek_i, self.tek_j, self.tek_new_i, self.tek_new_j, self.orientation)
                    self.tek_i, self.tek_j = self.tek_new_i, self.tek_new_j
                    if self.list_answers[self.tek_i][self.tek_j] == 1:
                        self.number_wrong_answers += 1
                else:
                    self.draw_bot_error(self.tek_i, self.tek_j, self.tek_i, self.tek_j, self.orientation)
                    self.number_errors += 1
            elif self.route[i] == 3:
                self.orientation -= 1
                self.orientation = 3 - (3 - self.orientation) % 4
                self.draw_bot(self.tek_i, self.tek_j, self.tek_i, self.tek_j, self.orientation)
            pygame.time.delay(400)
            pygame.display.flip()
        # Проверка достижения финишной ячейки
        if self.tek_i == self.finish_i and self.tek_j == self.finish_j:
            self.end_round = True
            # Подсчёт количества набранных баллов
            font_0 = pygame.font.SysFont('Comic Sans MS', 20)
            self.number_points = self.number_points + \
                                 int((4 * self.number_passed_cells) / (self.number_attempts +
                                 self.number_wrong_answers - 1) - self.number_errors)
            text_4 = font_0.render('Количество попыток: {}'.format(self.number_attempts), 1, black)
            screen.blit(text_4, (670, 200))
            text_4 = font_0.render('Количество ошибок: {}'.format(abs(self.number_errors -
                                                                  self.number_wrong_answers + 1)), 1, black)
            screen.blit(text_4, (670, 230))
            text_4 = font_0.render('Очки за заезд: {}'.format(self.number_points), 1, black)
            screen.blit(text_4, (670, 260))
            self.draw_bot_victory(self.tek_i, self.tek_j, self.tek_i, self.tek_j, self.orientation)
            pygame.time.delay(1000)
        self.start_motion = False
        self.start_new_i, self.start_new_j = self.tek_i, self.tek_j
        self.orientation_first_new = self.orientation
        self.route = []
        self.tek_i, self.tek_j = self.start_new_i, self.start_new_j


    # вывод заставки на победу игрока
    def win(self):
        for i in range(25):
            screen.fill((random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)))
            pygame.time.delay(80)
            pygame.display.flip()
        for i in range(100):
            color = (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
            x = random.randint(0, 940)
            y = random.randint(0, 740)
            r = random.randint(10, 250)
            pygame.draw.ellipse(screen, color, (x, y, r, r))
            pygame.time.delay(50)
            pygame.display.flip()
        pygame.time.delay(250)
        font_1 = pygame.font.SysFont('mistral', 80)
        text_1 = font_1.render('Победа!!!', 1, red)
        screen.blit(text_1, (300, 100))
        font_1 = pygame.font.SysFont('mistral', 70)
        text_1 = font_1.render('Урр-а!!! Благодарю тебя мой друг!', 1, white)
        screen.blit(text_1, (100, 200))
        text_1 = font_1.render('Ты помог достичь цели!', 1, white)
        screen.blit(text_1, (150, 300))
        text_1 = font_1.render('Количество набранных очков: {}'.format(number_points), 1, white)
        screen.blit(text_1, (100, 400))
        pygame.display.flip()
        pygame.time.delay(10000)


def get_cell(mouse_pos):
    cell_x = (mouse_pos[0] - 665) // 85
    cell_y = (mouse_pos[1] - 475) // 85
    if cell_x < 0 or cell_x > 2 or cell_y < 0 or cell_y > 2:
        return None
    return cell_x, cell_y


game = Game()
# основной цикл программы
running = True
while running:
    clock.tick(FPS)
    if game.start_motion:
        game.robot_motion()
        if game.end_round:
            number_points += game.number_points
            if number_points < points_to_win:
                number_round += 1
                game = Game()
            else:
                game.win()
                running = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            p = get_cell(event.pos)
            if p == (0, 2):
                game.indication_commands(5)
                game = Game()
            elif p == (1, 0):
                game.route.append(0)
                game.indication_commands(0)
            elif p == (2, 1):
                game.route.append(1)
                game.indication_commands(1)
            elif p == (1, 2):
                game.route.append(2)
                game.indication_commands(2)
            elif p == (0, 1):
                game.route.append(3)
                game.indication_commands(3)
            elif p == (1, 1):
                game.route.append(4)
                game.indication_commands(4)
                game.start_motion = True
            elif p == (2, 2):
                running = False
        if event.type == pygame.KEYDOWN:
            if event.key == 273:
                game.route.append(0)
                game.indication_commands(0)
            elif event.key == 275:
                game.route.append(1)
                game.indication_commands(1)
            elif event.key == 274:
                game.route.append(2)
                game.indication_commands(2)
            elif event.key == 276:
                game.route.append(3)
                game.indication_commands(3)
            elif event.key == 13 or event.key == 271:
                game.start_motion = True
                game.indication_commands(4)
            elif event.key == 32:
                game.indication_commands(5)
                game = Game()
            elif event.key == 27:
                running = False
    pygame.display.flip()
pygame.quit()