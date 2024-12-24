import random
from typing import List
from custom.customclasses import meditationClassifier


def search_meditation_on_key(searchkey: str, allmeditations: List[meditationClassifier]):
    meditations_to_return = []
    for meditation in allmeditations:
        add = False
        if searchkey in meditation.name:
            add = True
        else:
            for categories in meditation.type:
                if searchkey in categories:
                    add = True
        if add == True:
            meditations_to_return.append(meditation)
    return random.shuffle(meditations_to_return)

