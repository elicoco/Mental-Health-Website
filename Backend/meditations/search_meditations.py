from Backend.custom.customclasses import MeditationClassifier

meditationClassifiers = [
    MeditationClassifier(id=1,
                         filename="meditation-blue-138131.mp3",
                         type=["Sleep","Breathing"], length=81,
                         name="Breathing for Sleep") ,

    MeditationClassifier(id=2,
                         filename="meditation-blue-138131.mp3",
                         type=["Awareness", "Breathing"],
                         length=300,
                         name="Mindful Breath Awareness"),
    
    MeditationClassifier(id=3,
                         filename="meditation-blue-138131.mp3",
                         type=["Sleep", "Energy"],
                         length=450,
                         name="Restful Recharge Meditation"),
    
    MeditationClassifier(id=4,
                         filename="meditation-blue-138131.mp3",
                         type=["Breathing", "Energy"],
                         length=200,
                         name="Invigorating Breathwork"),
    
    MeditationClassifier(id=5,
                         filename="meditation-blue-138131.mp3",
                         type=["Sleep", "Awareness"],
                         length=600,
                         name="Drifting into Sleep"),
    
    MeditationClassifier(id=6,
                         filename="meditation-blue-138131.mp3",
                         type=["Awareness", "Energy"],
                         length=720,
                         name="Awakening Inner Vitality"),
    
    MeditationClassifier(id=7,
                         filename="meditation-blue-138131.mp3",
                         type=["Breathing", "Sleep"],
                         length=180,
                         name="Calm Breathing for Rest"),
    
    MeditationClassifier(id=8,
                         filename="meditation-blue-138131.mp3",
                         type=["Energy", "Breathing"],
                         length=150,
                         name="Energizing Morning Breath"),
    
    MeditationClassifier(id=9,
                         filename="meditation-blue-138131.mp3",
                         type=["Awareness", "Sleep"],
                         length=500,
                         name="Deep Relaxation Awareness"),
    
    MeditationClassifier(id=10,
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

def search_meditation_on_key(search_key: str):
    meditations_to_return = []
    search_key = search_key.lower()
    for meditation in meditationClassifiers:
        add = False
        if search_key in meditation.name.lower():
            add = True
        else:
            for categories in meditation.type:
                if search_key in categories.lower():
                    add = True
        if add:
            meditations_to_return.append(meditation)
    return meditations_to_return

