##############################################################################
# Class representing the menu where the user can choose actions to do (CRUD) #
##############################################################################
from Controllers.MenuController import MenuController


class Menu:
    def __init__(self):
        self.categories = ['Ingredient', 'Meal', 'Shopping list']
        self.options = ['Create', 'Set', 'Delete', 'Display']
        self.choices = {}
        self.inputs = [{}]
        self.controller = MenuController()

    @staticmethod
    def welcome():
        print('Welcome to the ShoppingListGenerator.\nThis software allows you to manage ingredients and meals to generate'
              'randomly a shopping list for the number of days wished.')

    def ask_choices(self):
        """
            Depending on the Menu attributes, display the menu and ask the user what actions to do and add it to the 
            choices for future actions
        """
        self.choices = {}
        while not self.in_scope():
            print('Which category would you like to browse ?')
            for category in self.categories:
                print('{}) - {}'.format(str(self.categories.index(category)), category))
            cat_choice = int(raw_input('Choose the category : '))
            print('You have chosen the {} category'.format(self.categories[cat_choice].lower()) if self.in_scope()
                  else 'The option {} is not available.'.format(str(cat_choice)))
        while not self.in_scope():
            print('Which action would you like to do ?')
            for action in self.options:
                print('{}) - {}'.format(str(self.options.index(action)), action))
                opt_choice = int(raw_input('Choose the action : '))
                print('You want to {}'.format(self.options[opt_choice].lower()) if self.in_scope()
                      else 'The option {} is not available.'.format(str(opt_choice)))
        self.choices['category'] = cat_choice
        self.choices['option'] = opt_choice

    def ask_inputs(self):
        """
            From an index of a category and an index of an option, asks the information concerning the target to the
            user and add it to the inputs if action = Display, no input needed => return
        """
        self.inputs = [{}]
        if not self.in_scope():
            raise ValueError('The category or the action number is not valid.')
        if self.choices['option'] == 3:
            return
        action = self.options[self.choices['option']].lower()
        if self.choices['category'] == 0:
            prefix_str = 'Name of the ingredient to {} : '
            self.inputs[0]['name_ingredient'] = raw_input(prefix_str.format(action))
        elif self.choices['category'] == 1:
            prefix_str = 'Name of the meal to {} : '
            self.inputs[0]['name_meal'] = raw_input(prefix_str.format(action))
        elif self.choices['category'] == 2:
            prefix_str = 'Id of the shopping list to {} : '
            self.inputs[0]['id_shoppinglist'] = raw_input(prefix_str.format(action))
    
    def ask_meal_adding(self):

        print('Press !c plus enter at any time to cancel current adding.\nPress !x plus enter at any time '
              'to stop adding ingredients')
        name_ingredient = ''
        quantity = 0
        while name_ingredient != '!x' and quantity != '!x':
            name_ingredient = raw_input('Name of the ingredient : ')
            if name_ingredient == '!c':
                continue
            elif name_ingredient == '!x':
                break
            quantity = int(raw_input('Quantity : '))
            if quantity == '!c':
                continue
            elif quantity == '!x':
                break
            self.inputs.append({'name_ingredient': name_ingredient, 'quantity': quantity})
            print('Successfully added.')

    def in_scope(self):
        """
            Return depending on the fact that the category and option are in bounds or not
            :return: True if the index of the category or option or both are not out of bounds else False
        """
        if self.choices['category'] is not None and self.choices['option'] is not None:
            return 0 <= self.choices['category'] < len(self.categories) and 0 < self.choices['option'] < len(self.options)
        elif self.choices['category'] is not None:
            return 0 <= self.choices['category'] < len(self.categories)
        elif self.choices['option'] is not None:
            return 0 <= self.choices['option'] < len(self.options)
        else:
            return False
