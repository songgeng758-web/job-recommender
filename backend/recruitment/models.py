from django.db import models

# 用户表
class User(models.Model):
    ROLE_CHOICES = [('seeker', '求职者'), ('hr', '企业HR'), ('admin', '管理员')]
    username = models.CharField(max_length=50, unique=True, verbose_name='用户名')
    password = models.CharField(max_length=255, verbose_name='密码')
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, verbose_name='角色')
    phone = models.CharField(max_length=20, blank=True, verbose_name='手机号')
    email = models.CharField(max_length=100, blank=True, verbose_name='邮箱')
    is_active = models.BooleanField(default=True, verbose_name='是否启用')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.username}({self.role})"

    class Meta:
        verbose_name = '用户'

# 企业表
class Company(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='HR账号')
    company_name = models.CharField(max_length=100, verbose_name='企业名称')
    industry = models.CharField(max_length=50, blank=True, verbose_name='所属行业')
    size = models.CharField(max_length=50, blank=True, verbose_name='企业规模')
    description = models.TextField(blank=True, verbose_name='企业简介')
    address = models.CharField(max_length=200, blank=True, verbose_name='企业地址')
    website = models.CharField(max_length=200, blank=True, verbose_name='企业官网')

    def __str__(self):
        return self.company_name

    class Meta:
        verbose_name = '企业'

# 简历表
class Resume(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='resumes', verbose_name='求职者')
    title = models.CharField(max_length=100, default='默认简历', verbose_name='简历名称')
    is_active = models.BooleanField(default=False, verbose_name='是否当前启用')

    real_name = models.CharField(max_length=50, blank=True, verbose_name='姓名')
    school = models.CharField(max_length=100, blank=True, verbose_name='学校')
    major = models.CharField(max_length=100, blank=True, verbose_name='专业')
    degree = models.CharField(max_length=20, blank=True, verbose_name='学历')
    education_exp = models.TextField(blank=True, verbose_name='教育经历')
    work_exp = models.TextField(blank=True, verbose_name='工作经历')
    skills = models.TextField(blank=True, verbose_name='技能描述')
    expect_job = models.CharField(max_length=100, blank=True, verbose_name='期望岗位')
    expect_city = models.CharField(max_length=50, blank=True, verbose_name='期望城市')
    expect_salary = models.CharField(max_length=50, blank=True, verbose_name='期望薪资')
    self_intro = models.TextField(blank=True, verbose_name='自我评价')
    project_exp = models.TextField(blank=True, verbose_name='项目经历')
    certificate_exp = models.TextField(blank=True, verbose_name='证书与校园经历')
    content_text = models.TextField(blank=True, verbose_name='推荐用拼接文本')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}-{self.title}"

    class Meta:
        verbose_name = '简历'

# 职位表
class Job(models.Model):
    STATUS_CHOICES = [('pending','待审核'), ('approved','已发布'), ('rejected','已拒绝'), ('offline','已下线')]
    hr = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='发布HR')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, null=True, blank=True, verbose_name='所属企业')
    title = models.CharField(max_length=100, verbose_name='职位名称')
    city = models.CharField(max_length=50, blank=True, verbose_name='工作城市')
    salary_min = models.IntegerField(default=0, verbose_name='最低薪资')
    salary_max = models.IntegerField(default=0, verbose_name='最高薪资')
    job_type = models.CharField(max_length=20, blank=True, verbose_name='工作类型')
    degree_required = models.CharField(max_length=20, blank=True, verbose_name='学历要求')
    exp_required = models.CharField(max_length=50, blank=True, verbose_name='经验要求')
    description = models.TextField(blank=True, verbose_name='职位描述')
    skill_required = models.TextField(blank=True, verbose_name='技能要求')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = '职位'

# 投递表
class Application(models.Model):
    STATUS_CHOICES = [('pending','待查看'), ('viewed','已查看'), ('interview','面试'), ('rejected','不合适'), ('hired','录用')]
    job = models.ForeignKey(Job, on_delete=models.CASCADE, verbose_name='职位')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='求职者')
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, null=True, blank=True, verbose_name='简历')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending', verbose_name='状态')
    apply_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} 投递了 {self.job.title}"

    class Meta:
        verbose_name = '投递记录'