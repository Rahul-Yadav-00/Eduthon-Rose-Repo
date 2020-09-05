from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.
class ClassRoom(models.Model):
    classname = models.CharField(max_length = 50)
    classsubject = models.CharField(max_length = 30)
    teacher = models.ForeignKey(User,on_delete = models.CASCADE,related_name='teacher_of_class')
    classCode = models.SlugField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    classdecription = models.TextField()

    def __str__(self):
        return self.classname + " by " + self.teacher.username

    def save(self,*args,**kwargs):
        if(self.classCode == None):
            classcode = slugify(self.classname)
            has_classcode = ClassRoom.objects.filter(classCode = classcode).exists()
            count = 1
            while has_classcode:
                count += 1
                classcode = slugify(self.classname) + '-' + str(count)
                has_classcode = ClassRoom.objects.filter(classCode = classcode).exists()
            
            self.classCode = classcode
        super().save(*args,**kwargs)


class ClassStudents(models.Model):
    student = models.ForeignKey(User,on_delete = models.CASCADE,related_name = 'student_who_join')
    classroom = models.ForeignKey(ClassRoom,on_delete = models.CASCADE,related_name = 'which_classroom_join')

    class Meta:
        unique_together = ['student','classroom']
    def __str__(self):
        return f'{self.student.username} in {self.classroom.classname}'


class Chat(models.Model):
    classroom = models.ForeignKey(ClassRoom,on_delete = models.CASCADE,related_name='chats')
    body = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User,on_delete = models.CASCADE)

    class Meta:
        ordering = ['created']

    def __str__ (self):
        return f'comment by {self.user.username}'



class ClassTest(models.Model):
    classroom = models.ForeignKey(ClassRoom,on_delete = models.CASCADE,related_name='classTest')
    name = models.CharField(max_length = 50)
    testTopic = models.CharField(max_length = 200)
    created = models.DateTimeField(auto_now_add = True)
    testCode =  models.SlugField(null=True, blank=True)

    class Meta:
        ordering = ['created']

    def save(self,*args,**kwargs):
        if(self.testCode == None):
            testcode = slugify(self.testTopic)
            has_testcode = ClassTest.objects.filter(testCode = testcode).exists()
            count = 1
            while has_testcode:
                count += 1
                testcode = slugify(self.testTopic) + '-' + str(count)
                has_testcode = ClassTest.objects.filter(testCode = testcode).exists()
            
            self.testCode = testcode
        super().save(*args,**kwargs)

    def __str__(self):
        return f'{self.name} in {self.classroom.classname}'

class MCQuestion(models.Model):
    test = models.ForeignKey(ClassTest,on_delete = models.CASCADE,related_name='testquestion')
    question = models.TextField()
    option_a = models.TextField()
    option_b = models.TextField()
    option_c = models.TextField()
    option_d = models.TextField()
    choice = (('a',option_a),('b',option_b),('c',option_c),('d',option_d))
    answer = models.CharField(max_length=1,choices = choice )
    questionCode =  models.SlugField(null=True, blank=True)

    def save(self,*args,**kwargs):
        if(self.questionCode == None):
            questioncode = slugify(self.question)
            has_code = MCQuestion.objects.filter(questionCode = questioncode).exists()
            count = 1
            while(has_code):
                count += 1
                questioncode = slugify(self.question) + '-' + str(count)
                has_code = MCQuestion.objects.filter(questionCode = questioncode).exists()
            
            self.questionCode = questioncode
            super().save(*args,**kwargs)
    def __str__(self):
        return self.questionCode