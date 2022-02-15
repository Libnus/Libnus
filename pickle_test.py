import pickle

animals = {'tiger': 23, 'lion': 45, 'giraffe': 67}

f = open('data.pickle', 'wb')
pickle.dump(animals, f)
f.close()

f = open('data.pickle', 'rb')
unpickled_animals = pickle.load(f)
f.close()
print(unpickled_animals)
