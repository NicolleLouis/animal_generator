from animal_generator.models.experience import Experience
from animal_generator.services.ecosystem_viewer import EcosystemViewer
from animal_generator.services.zoo_viewer import ZooViewer

rabbit = ZooViewer.find_animal("rabbit")
meadow = EcosystemViewer.find_ecosystem("meadow")
experience = Experience(meadow, rabbit)
experience.run()
print(rabbit.fitness_score)
