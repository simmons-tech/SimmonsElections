from django.db import models

class Resident(models.Model):
    athena = models.CharField(max_length=30, unique=True)

    def __unicode__(self):
        return self.athena

class Poll(models.Model):
    question = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.question

class Choice(models.Model):
    poll = models.ForeignKey(Poll)
    choice = models.CharField(max_length=200)
    
    def num_first_selected(self):
        return len(AnswerSet.objects.filter(first_choice=self, active=True))
    
    def num_second_selected(self):
        return len(AnswerSet.objects.filter(second_choice=self, active=True))
    
    def num_third_selected(self):
        return len(AnswerSet.objects.filter(third_choice=self, active=True))
    
    def __unicode__(self):
        return self.choice

class AnswerSet(models.Model):
    name = models.CharField(max_length=200)
    question = models.ForeignKey(Poll)
    first_choice = models.ForeignKey(Choice, related_name='first', null=True, blank=True)
    second_choice = models.ForeignKey(Choice, related_name='second', null=True, blank=True)
    third_choice = models.ForeignKey(Choice, related_name='third', null=True, blank=True)
    active = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
    
    def __unicode__(self):
        return self.name + " answering " + str(self.question) + " at " + str(self.created)
        
    def get_answers(self):
        return 'first=' + str(self.first_choice) + ', second=' + str(self.second_choice) + ', third=' + str(self.third_choice)

    def nonempty(self):
        return self.first_choice != None
        

    def get_choice(self, i):
        if i == 1:
            return self.first_choice
        elif i == 2:
            return self.second_choice
        elif i == 3:
            return self.third_choice
        else:
            raise ValueError("i in get_choice must be in [1,3]")

    def is_valid(self):
        if self.get_choice(3) and not self.get_choice(2):
            return False
        if self.get_choice(2) and not self.get_choice(1):
            return False

        unique_choices = set()
        for i in range(1,4):
            choice = self.get_choice(i)
            if choice and choice in unique_choices:
                # Voted for someone twice
                return False
            unique_choices.add(choice)
        return True

                
        
