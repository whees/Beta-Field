# -*- coding: utf-8 -*-
"""
Created on Sat Oct  5 20:57:31 2024

@author: lcuev
"""
import pygame
from librarian import Librarian
from numpy import tanh

black = (0, 0, 0)
pink = (255, 0, 255)
green = (0, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
purple = (255, 255, 0)
orange = (0, 255, 255)
feet = 0
start = 1
middle = 2
finish = 3
erase = 4
recall = 5
colors = {feet: pink, start: green, middle: blue,
          finish: red, erase: purple, recall: orange}
names = {feet: 'feet', start: 'start',
         middle: 'middle', finish: 'finish', erase: 'erase'}
neuron_length = 4
neuron_area = neuron_length * (neuron_length - 1) // 2
length = 498
area = length * (length - 1) // 2


class BetaField:
    def __init__(self):
        self.dict = self.get_dict(area)
        self.neuron_dict = self.get_dict(neuron_area)
        self.weights = [[0 for n in range(neuron_area)] for a in range(area)]
        self.memory_count = 0

    def get_dict(self, length):
        dict = {}
        for i in range(length):
            dict[i] = self.unflatten(i)
        return dict

    def unflatten(self, index):
        f = int(0.5 * (8 * index + 1) ** 0.5 + 0.5)
        return f, index - f * (f - 1) // 2

    def flatten(self, left, right=0):
        return left * (left - 1) // 2 + right

    def copy(self, arr):
        return [[arr[i][j] for j in range(neuron_length)] for i in range(length)]

    def activate(self, input):
        for i in range(length):
            for j in range(neuron_length):
                input[i][j] = tanh(input[i][j])
        return input

    def memorize(self, output):
        self.memory_count += 1
        for key, value in self.dict.items():
            left, right = value
            for n_key, n_value in self.neuron_dict.items():
                n_left, n_right = n_value
                self.weights[key][n_key] += output[left][n_left] * \
                    output[right][n_right]

    def recall(self, input):
        rate = self.memory_count ** -1
        output = self.copy(input)
        for key, value in self.dict.items():
            left, right = value
            for n_key, n_value in self.neuron_dict.items():
                n_left, n_right = n_value
                output[left][n_left] += self.weights[key][n_key] * \
                    input[right][n_right] * rate
                output[right][n_right] += self.weights[key][n_key] * \
                    input[left][n_left] * rate
        return self.activate(output)


class GUI:
    def __init__(self, size):
        self.size = size
        self.surface = pygame.display.set_mode((size,) * 2)
        self.running = True
        self.librarian = Librarian()
        self.wood_img = pygame.transform.scale(pygame.image
                                               .load('C:/Users/lcuev/Documents/Beta-Field/img/wood.png'),
                                               (size, size)).convert_alpha()
        self.plastic_img = pygame.transform.scale(pygame.image
                                                  .load('C:/Users/lcuev/Documents/Beta-Field/img/plastic.png'),
                                                  (size, size)).convert_alpha()
        self.places = {}
        self.mode = 1
        self.toggle_hold = False
        self.betafield = BetaField()
        pygame.display.set_caption('Beta-Field')

    def get_array(self):
        array = [[-1 for j in range(4)] for i in range(area)]

        for key, value in self.places.items():
            array[key][value] = 1

        return array

    def get_places(self, array):
        places = {}

        for i in range(length):
            for j in range(neuron_length):
                if array[i][j] > 0:
                    places[i] = j
                    break

        return places

    def project_to_board(self, pos):
        return (round(136 * (pos[0] / self.size - 0.5) / 4) * 4,  round(144 * (1 - pos[1] / self.size) / 4) * 4)

    def project_to_screen(self, pos):
        return (int((pos[0] / 136 + 0.5) * self.size), int((1 - pos[1] / 144) * self.size))

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.toggle_hold = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.mode = erase
                if event.key == pygame.K_f:
                    self.mode = feet
                if event.key == pygame.K_s:
                    self.mode = start
                if event.key == pygame.K_m:
                    self.mode = middle
                if event.key == pygame.K_p:
                    self.mode = finish
                if event.key == pygame.K_r:
                    self.mode = recall
                if event.key == pygame.K_c:
                    self.places = {}
                if event.key == pygame.K_a:
                    self.betafield.memorize(self.get_array())

    def update(self):
        if self.mode == recall:
            self.places = self.get_places(
                self.betafield.recall(self.get_array()))
        elif self.toggle_hold:
            mouse_position = pygame.mouse.get_pos()
            board_position = self.project_to_board(mouse_position)
            hold = self.librarian.places.get(board_position)

            if hold is not None:
                if self.mode in range(4):
                    self.places[hold] = self.mode
                else:
                    self.places.pop(hold, None)

            self.toggle_hold = False

    def display(self):
        self.surface.fill(black)
        self.surface.blit(self.wood_img, (0, 0))
        self.surface.blit(self.plastic_img, (0, 0))

        for key, value in self.places.items():
            board_position = self.librarian.revplaces[key]
            screen_position = self.project_to_screen(board_position)
            pygame.draw.circle(
                self.surface, colors[value], screen_position, 20, width=4)

        mouse_position = pygame.mouse.get_pos()
        pygame.draw.circle(
            self.surface, colors[self.mode], mouse_position, 10)
        pygame.display.update()

    def main_loop(self):
        self.handle_events()
        self.update()
        self.display()
        return self.running


if __name__ == '__main__':
    pygame.init()
    gui = GUI(1000)
    while gui.main_loop():
        pass
    pygame.quit()
