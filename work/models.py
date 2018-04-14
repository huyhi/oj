from django.db import models

from auth_system.models import MyUser


class BanJi(models.Model):
    """
    班级
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40, verbose_name='班级名称')
    teacher = models.ForeignKey(MyUser, null=True, related_name='banJi_teacher')
    students = models.ManyToManyField(MyUser, related_name='banJi_students')
    courser = models.ForeignKey('judge.ClassName', null=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()

    def __str__(self):
        return str(self.name)


class HomeWork(models.Model):
    """
    公共作业
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    courser = models.ForeignKey('judge.ClassName', verbose_name='所属课程')
    creater = models.ForeignKey(MyUser, verbose_name='创建者')
    start_time = models.DateTimeField(verbose_name='开始时间')
    end_time = models.DateTimeField(verbose_name='结束时间')
    problem_ids = models.CharField(max_length=200, verbose_name='编程题列表id列表')
    choice_problem_ids = models.CharField(max_length=200, verbose_name='选择题id列表', null=True, blank=True)
    gaicuo_problem_ids = models.CharField(max_length=200, verbose_name='改错题列表id列表',null=True)
    tiankong_problem_ids = models.CharField(max_length=200, verbose_name='填空题列表id列表',null=True)
    problem_info = models.TextField()
    choice_problem_info = models.TextField()
    tiankong_problem_info = models.TextField(null=True)
    gaicuo_problem_info = models.TextField(null=True)
    allowed_languages = models.CharField(max_length=50)
    work_kind = models.CharField(max_length=20,verbose_name="作业类型",default='作业')
    total_score = models.IntegerField()
    allow_resubmit = models.BooleanField(default=True, verbose_name='是否允许重复提交作业>？')
    allow_similarity = models.BooleanField(default=True, verbose_name='是否开启相似度判分>？')
    def __str__(self):
        return str(self.id)


class MyHomework(models.Model):
    """
    私有作业
    """
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    courser = models.ForeignKey('judge.ClassName', verbose_name='所属课程')
    creater = models.ForeignKey(MyUser, verbose_name='创建者')
    #numid = models.ForeignKey('MyUser.id_num', verbose_'学号/工号')
    start_time = models.DateTimeField(verbose_name='开始时间')
    end_time = models.DateTimeField(verbose_name='结束时间')
    problem_ids = models.CharField(max_length=200, verbose_name='编程题列表id列表', null=True, blank=True)
    choice_problem_ids = models.CharField(max_length=200, verbose_name='选择题id列表', null=True, blank=True)
    gaicuo_problem_ids = models.CharField(max_length=200, verbose_name='改错题列表id列表',null=True)
    tiankong_problem_ids = models.CharField(max_length=200, verbose_name='填空题列表id列表',null=True)
    problem_info = models.TextField(null=True, blank=True)
    choice_problem_info = models.TextField(null=True, blank=True)
    gaicuo_problem_info = models.TextField(null=True, blank=True)
    tiankong_problem_info = models.TextField(null=True, blank=True)
    allowed_languages = models.CharField(max_length=50)
    banji = models.ManyToManyField(BanJi)
    finished_students = models.ManyToManyField(MyUser, related_name='finished_students', blank=True)
    allow_resubmit = models.BooleanField(default=True, verbose_name='是否允许重复提交作业？')
    allow_random = models.BooleanField(default=True, verbose_name='是否打乱选择题选项顺序？')
    allow_similarity = models.BooleanField(default=False, verbose_name='是否开启相似度判分？')
    work_kind = models.CharField(max_length=20,verbose_name="作业类型",default='作业')
    total_score = models.IntegerField()

    def __str__(self):
        return str(self.id)


class HomeworkAnswer(models.Model):
    """
    保存用户提交作业后的相关信息
    """
    id = models.AutoField(primary_key=True)
    homework = models.ForeignKey(MyHomework, null=True, verbose_name='作业')
    creator = models.ForeignKey(MyUser, null=True, verbose_name='答题者')
    wrong_choice_problems = models.CharField(max_length=200, null=False, verbose_name='错误的选择题', default='')  #
    wrong_choice_problems_info = models.CharField(max_length=200, null=False, verbose_name='错误的选择题保留信息', default='')
    score = models.IntegerField(null=False, verbose_name='总成绩', default=0)
    choice_problem_score = models.IntegerField(null=False, verbose_name='选择题成绩', default=0)
    problem_score = models.IntegerField(null=False, verbose_name='编程题成绩', default=0)
    tiankong_score = models.IntegerField(null=False, verbose_name='程序填空题成绩', default=0)
    gaicuo_score = models.IntegerField(null=False, verbose_name='程序改错题成绩', default=0)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name='答题时间')
    judged = models.BooleanField(default=False, verbose_name='是否已经判分？')
    summary = models.TextField(null=True, verbose_name='实验小结')
    teacher_comment = models.TextField(null=True, verbose_name='教师评语')

    def __str__(self):
        return str(self.id)


class TempHomeworkAnswer(models.Model):
    """暂存表单数据"""
    id = models.AutoField(primary_key=True)
    homework = models.ForeignKey(MyHomework)
    creator = models.ForeignKey(MyUser)
    data = models.TextField(null=True)
