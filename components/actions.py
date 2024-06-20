from definitions import needs

class Action:

    def __init__(self, name, time=None, sub_actions=None, satisfies=None, factor=None):

        self._name = name
        self._time = time
        self._sub_actions = sub_actions
        self._satisfies = satisfies
        self._factor = factor

move = Action('move', time='function')
consume_water = Action('consume_water', time=0, satisfies=needs.water, factor)
consume_food = Action('consume_food', time=0, satisfies=needs.food, factor)
take = Action('take', time=0)
store = Action('store', time=0)
find_animals = Action('find_animals', time='ability+random?')
attack = Action('attack', time='ability')

base_actions = [
    move,
    consume_water,
    take,
    store,
    find_animals,
    attack,
]

collect_water = Action('collect_water', sub_actions=[move, consume_water, take, move, store])
hunt = Action('hunt', sub_actions=[move, find_animals, attack, take, move, store])

