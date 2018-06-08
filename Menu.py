##############################################################################
# Class representing the menu where the user can choose actions to do (CRUD) #
##############################################################################


class Menu:
    def __init__(self):
        self.categories = ['Ingredient', 'Meal', 'Shopping list']
        self.options = ['Create', 'Set', 'Delete', 'Display']

    @staticmethod
    def welcome():
        print('Welcome to the ShoppingListGenerator.\nThis software allows you to manage ingredients and meals to generate'
              'randomly a shopping list for the number of days wished.')

    def ask_action(self):
        """
            Depending on the Menu attributes, display the menu and ask the user what actions to do and returns it
            :return: cat_choice, act_choice : the index of the category and the action the user want to do
        """
        cat_choice, act_choice = -1
        while not self.in_scope(cat=cat_choice):
            print('Which category would you like to browse ?')
            for category in self.categories:
                print('{}) - {}'.format(str(self.categories.index(category)), category))
            cat_choice = int(raw_input('Choose the category : '))
            print('You have chosen the {} category'.format(self.categories[cat_choice].lower()) if self.in_scope(cat=cat_choice)
                  else 'The option {} is not available.'.format(str(cat_choice)))
        while not self.in_scope(act=act_choice):
            print('Which action would you like to do ?')
            for action in self.options:
                print('{}) - {}'.format(str(self.options.index(action)), action))
                act_choice = int(raw_input('Choose the action : '))
                print('You want to {}'.format(self.options[act_choice].lower()) if self.in_scope(act=act_choice)
                      else 'The option {} is not available.'.format(str(act_choice)))
        return cat_choice, act_choice

    def ask_action_target(self, cat, act):
        """
            From an index of a category and an index of an action, asks the information concerning the target to the user
            if action = Display, no inputs needed
            :param cat: the index of the category in which operate
            :param act: the index of the action to do
            :return: inputs : the information concerning the category and the action to proceed and the inputs from the user
        """
        inputs = {'action': (cat, act)}
        if not self.in_scope(cat, act):
            raise ValueError('The category or the action number is not valid.')
        if self.options[act] == 'Display':
            return inputs
        action = self.options[cat][act].lower()
        if cat == 0:
            prefix_str = 'Name of the ingredient to {} :'
            inputs['name_ingredient'] = raw_input(prefix_str.format(action))
        elif cat == 1:
            prefix_str = 'Name of the meal to {} :'
            inputs['name_meal'] = raw_input(prefix_str.format(action))
        elif cat == 2:
            prefix_str = 'Id of the shopping list to {}'
            inputs['id_shoppinglist'] = raw_input(prefix_str.format(action))
        return inputs

    def in_scope(self, cat=None, act=None):
        """
            Return depending on the fact that indexes in parameters are in bounds or not
            :param ? cat : the index of the category
            :param ? act : the index of the action
            :return: True if the index of cat or act or both are not out of bounds else False
        """
        if cat is not None and act is not None:
            return 0 <= cat < len(self.categories) and 0 < act < len(self.options)
        elif cat is not None:
            return 0 <= cat < len(self.categories)
        elif act is not None:
            return 0 <= act < len(self.options)
        else:
            raise ValueError('You must at least give a category or an action number in parameter.')