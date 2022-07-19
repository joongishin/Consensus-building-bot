"""
A class for forming a dialogue
"""


class DialogueHandler:
    def __init__(self):
        self.needs = []
        self.ideas = []
        self.votes = []
        self.current_direction = ''
        self.personal_idea = ''
        self.conflict_index = 0


dh = DialogueHandler()

# Sample conflicts, opinions, and rationales.
dh.needs = [
    ['*Student group A wants to have team projects*',
     '*Student group B does not want to have team projects*'],
    ['*Student group C wants to have their own topics for projects*',
     '*Student group D wants to have topics assigned by teachers*']
]

dh.ideas = [
    ['\"Let students do team projects by themselves if they want.\"\n',
     '\"Adjust the number of team projects.\"\n',
     '\"Give students more freedom for forming a team.\"\n'],
    ['\"Allow students to find and select their own topics only with the teacher’s confirmation.\"\n',
     '\"Have a discussion between students and teachers to have a set of topics for the projects.\"\n',
     '\"Have two smaller projects so that students get the chances to choose their own topics but also to work on the topics from the teachers.\"\n']
]

dh.votes = [
    ['\"I think voting is already a fair procedure.\"\n',
     '\"There is no way to fully satisfy both sides without one side compromising own needs.\"\n',
     '\"I think voting is the more economic approach for everyone.\"\n'],
    ['\"Everyone would be already familiar with voting.\"\n',
     '\"At least one of the groups will be completely satisfied.\"\n',
     '\"I think voting is better than somewhat satisfying both groups.\"\n']
]

