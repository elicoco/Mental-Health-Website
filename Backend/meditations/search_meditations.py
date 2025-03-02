from Backend.custom.customclasses import meditationClassifier

meditationClassifiers = [
    meditationClassifier(id=1, 
            filename="meditation-blue-138131.mp3", 
            type=["Sleep","Breathing"], length=81, 
            name="Breathing for Sleep") ,

    meditationClassifier(id=2, 
        filename="meditation-blue-138131.mp3", 
        type=["Awareness", "Breathing"], 
        length=300, 
        name="Mindful Breath Awareness"),
    
    meditationClassifier(id=3, 
        filename="meditation-blue-138131.mp3", 
        type=["Sleep", "Energy"], 
        length=450, 
        name="Restful Recharge Meditation"),
    
    meditationClassifier(id=4, 
        filename="meditation-blue-138131.mp3", 
        type=["Breathing", "Energy"], 
        length=200, 
        name="Invigorating Breathwork"),
    
    meditationClassifier(id=5, 
        filename="meditation-blue-138131.mp3", 
        type=["Sleep", "Awareness"], 
        length=600, 
        name="Drifting into Sleep"),
    
    meditationClassifier(id=6, 
        filename="meditation-blue-138131.mp3", 
        type=["Awareness", "Energy"], 
        length=720, 
        name="Awakening Inner Vitality"),
    
    meditationClassifier(id=7, 
        filename="meditation-blue-138131.mp3", 
        type=["Breathing", "Sleep"], 
        length=180, 
        name="Calm Breathing for Rest"),
    
    meditationClassifier(id=8, 
        filename="meditation-blue-138131.mp3", 
        type=["Energy", "Breathing"], 
        length=150, 
        name="Energizing Morning Breath"),
    
    meditationClassifier(id=9, 
        filename="meditation-blue-138131.mp3", 
        type=["Awareness", "Sleep"], 
        length=500, 
        name="Deep Relaxation Awareness"),
    
    meditationClassifier(id=10, 
        filename="meditation-blue-138131.mp3", 
        type=["Energy", "Sleep"], 
        length=900, 
        name="Restorative Energy Sleep")
]

def get_all_meditations():
    return meditationClassifiers

def get_meditation_by_id(id):
    if (id.isdigit() == False or int(id) > len(meditationClassifiers) 
     or int(id) <= 0):
        return False
    else:
        id = int(id)
        return meditationClassifiers[id-1]
# returns meditation by an id

def search_meditation_on_key(searchkey: str):
    meditations_to_return = []
    searchkey = searchkey.lower()
    for meditation in meditationClassifiers:
        add = False
        if searchkey in meditation.name.lower():
            add = True
        else:
            for categories in meditation.type:
                if searchkey in categories.lower():
                    add = True
        if add == True:
            meditations_to_return.append(meditation)
    return meditations_to_return

