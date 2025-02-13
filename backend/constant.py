from rest_framework.exceptions import ValidationError
days_of_the_weeks = [
    ('lundi', 'Lundi'),
    ('mardi', 'Mardi'),
    ('mercredi', 'Mercredi'),
    ('jeudi', 'Jeudi'),
    ('vendredi', 'Vendredi'),
    ('samedi', 'Samedi'),
    ('dimanche', 'Dimanche'),
]

hours_of_the_day = [
    ('07h', '07h'),
    ('08h', '08h'),
    ('09h', '09h'),
    ('10h', '10h'),
    ('11h', '11h'),
    ('12h', '12h'),
    ('13h', '13h'),
    ('14h', '14h'),
    ('15h', '15h'),
    ('16h', '16h'),
    ('17h', '17h'),
]

currencies = [
    ('F CFA', 'F CFA')
]

systemes = [
    ('Congolais', 'Congolais')
]

statues = [
    ('Activé', 'Activé'),
    ('Desactivé', 'Desactivé')
]

months = [
    ('Janvier', 'Janvier'),
    ('Février', 'Février'),
    ('Mars', 'Mars'),
    ('Avril', 'Avril'),
    ('Mai', 'Mai'),
    ('Juin', 'Juin'),
    ('Juillet', 'Juillet'),
    ('Août', 'Août'),
    ('Septembre', 'Septembre'),
    ('Octobre', 'Octobre'),
    ('Novembre', 'Novembre'),
    ('Décembre', 'Décembre'),
]


last_diploma = (
    ('Doctorat', 'Doctorat'),
    ('Master', 'Master'),
    ('Licence', 'Licence'),
    ('DUT', 'DUT'),
    ('Baccalauréat', 'Baccalauréat')
)
cities = (
    ('pointe_noire', "Pointe Noire"),
    ('brazzaville', "Brazzaville")
)

type_blood = (
    ('O+', "O+"),
    ('O-', "O-"),
    ('A+', "A+"),
    ('A-', "A-"),
    ('B+', "B+"),
    ('B-', "B-"),
    ('AB+', "AB+"),
    ('AB-', "AB-"),
)

sexes = (
    ('masculin', 'Masculin'),
    ('feminin', 'Féminin')
)
cycles = (
    ('Primaire', 'Primaire'),
    ('College', 'College'),
    ('College Technique industrielle', ' College technique industrielle'),
    ('Lycée général', 'Lycée général'),
    ('Lycée technique commerciale', 'Lycée technique commerciale'),
    ('Lycée technique industrielle', 'Lycée technique industrielle')
)

types_of_classroom = (
    ('Primaire', 'Primaire'),
    ('College', 'College'),
    ('Lycée', 'Lycée')
)
types = [('Obligatoire', 'Obligatoire'), ('Secondaire', 'Secondaire')]


periode_of_exam = [
    ('Premier trimestre', 'Premier trimestre'),
    ('Deuxième trimestre', 'Deuxième trimestre'),
    ('Troisième trimestre', 'Troisième trimestre'),
    ('Janvier', 'Janvier'),
    ('Février', 'Février'),
    ('Mars', 'Mars'),
    ('Avril', 'Avril'),
    ('Mai', 'Mai'),
    ('Juin', 'Juin'),
    ('Juillet', 'Juillet'),
    ('Août', 'Août'),
    ('Septembre', 'Septembre'),
    ('Octobre', 'Octobre'),
    ('Novembre', 'Novembre'),
    ('Décembre', 'Décembre'),
]

do_classes = [
    ('Le matin', 'Le matin'),
    ('Midi', 'Midi'),
    ('Plein temps', 'Plein temps'),
]

types_evaluations = [
    ('Devoir de classe', 'Devoir de classe'),
    ('Examen', 'Examen')
]


def get_user_school(request):
    school = request.session.get('school')
    if not school:
        raise ValidationError({"detail": "École non trouvée."})
    return school