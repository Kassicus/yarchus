import pygame

import lib
import command

class Player():
    def __init__(self):
        self.inventory = []

    def add_to_inventory(self, item):
        self.inventory.append(item)

    def show_inventory(self, feedback_prompt):
        for item in self.inventory:
            line = command.FeedbackLine(item.name)
            feedback_prompt.feedback_lines.append(line)