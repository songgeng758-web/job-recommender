from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework import status
from .models import User, Job, Resume, Application, Company
from .serializers import (
    UserRegisterSerializer,
    JobSerializer,
    ResumeSerializer,
    ApplicationSerializer,
    CompanySerializer,
    UserListSerializer,
)
import hashlib


# ========== 用户注册 ==========
@api_view(['POST'])
def register(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'msg': '注册成功'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ========== 用户登录 ==========
@api_view(['POST'])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    pwd_md5 = hashlib.md5(password.encode()).hexdigest()
    try:
        user = User.objects.get(username=username, password=pwd_md5)
        return Response({
            'msg': '登录成功',
            'user_id': user.id,
            'username': user.username,
            'role': user.role,
        })
    except User.DoesNotExist:
        return Response({'msg': '用户名或密码错误'}, status=status.HTTP_400_BAD_REQUEST)


# ========== 职位列表 ==========
@api_view(['GET'])
def job_list(request):
    jobs = Job.objects.filter(status='approved')
    serializer = JobSerializer(jobs, many=True)
    return Response(serializer.data)


# ========== 职位详情 ==========
@api_view(['GET'])
def job_detail(request, job_id):
    try:
        job = Job.objects.get(id=job_id)
        serializer = JobSerializer(job)
        return Response(serializer.data)
    except Job.DoesNotExist:
        return Response({'msg': '职位不存在'}, status=status.HTTP_404_NOT_FOUND)


# ========== 发布职位 ==========
@api_view(['POST'])
def job_create(request):
    serializer = JobSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({'msg': '职位发布成功，等待审核'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ========== 当前启用简历（兼容旧页面） ==========
@api_view(['GET', 'POST'])
def my_resume(request):
    user_id = request.query_params.get('user_id') or request.data.get('user_id') or request.data.get('user')
    if not user_id:
        return Response({'msg': '缺少 user_id'}, status=status.HTTP_400_BAD_REQUEST)

    if request.method == 'GET':
        resume = Resume.objects.filter(user_id=user_id, is_active=True).first()
        if not resume:
            return Response({'msg': '当前没有启用简历'}, status=status.HTTP_404_NOT_FOUND)
        serializer = ResumeSerializer(resume)
        return Response(serializer.data)

    if request.method == 'POST':
        resume_id = request.data.get('id')
        if resume_id:
            try:
                resume = Resume.objects.get(id=resume_id, user_id=user_id)
            except Resume.DoesNotExist:
                return Response({'msg': '简历不存在'}, status=status.HTTP_404_NOT_FOUND)
            serializer = ResumeSerializer(resume, data=request.data, partial=True)
        else:
            resume = Resume.objects.filter(user_id=user_id, is_active=True).first()
            if resume:
                serializer = ResumeSerializer(resume, data=request.data, partial=True)
            else:
                data = request.data.copy()
                data['user'] = user_id
                data['is_active'] = True
                if not data.get('title'):
                    data['title'] = '默认简历'
                serializer = ResumeSerializer(data=data)

        if serializer.is_valid():
            serializer.save()
            return Response({'msg': '简历保存成功'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ========== 简历列表 ==========
@api_view(['GET'])
def resume_list(request):
    user_id = request.query_params.get('user_id')
    if not user_id:
        return Response({'msg': '缺少 user_id'}, status=status.HTTP_400_BAD_REQUEST)

    resumes = Resume.objects.filter(user_id=user_id).order_by('-is_active', '-updated_at', '-created_at')
    serializer = ResumeSerializer(resumes, many=True)
    return Response(serializer.data)


# ========== 新建简历 ==========
@api_view(['POST'])
def resume_create(request):
    data = request.data.copy()
    user_id = data.get('user_id') or data.get('user')
    if not user_id:
        return Response({'msg': '缺少 user_id'}, status=status.HTTP_400_BAD_REQUEST)

    data['user'] = user_id

    has_resume = Resume.objects.filter(user_id=user_id).exists()
    if 'is_active' not in data:
        data['is_active'] = not has_resume

    if not data.get('title'):
        count = Resume.objects.filter(user_id=user_id).count() + 1
        data['title'] = f'简历{count}'

    serializer = ResumeSerializer(data=data)
    if serializer.is_valid():
        resume = serializer.save()

        if resume.is_active:
            Resume.objects.filter(user_id=user_id).exclude(id=resume.id).update(is_active=False)

        return Response({'msg': '简历创建成功', 'id': resume.id}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ========== 简历详情 / 更新 ==========
@api_view(['GET', 'PUT', 'PATCH'])
def resume_detail(request, resume_id):
    try:
        resume = Resume.objects.get(id=resume_id)
    except Resume.DoesNotExist:
        return Response({'msg': '简历不存在'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = ResumeSerializer(resume)
        return Response(serializer.data)

    serializer = ResumeSerializer(resume, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response({'msg': '简历更新成功'})
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ========== 启用某份简历 ==========
@api_view(['POST'])
def activate_resume(request, resume_id):
    try:
        resume = Resume.objects.get(id=resume_id)
    except Resume.DoesNotExist:
        return Response({'msg': '简历不存在'}, status=status.HTTP_404_NOT_FOUND)

    Resume.objects.filter(user_id=resume.user_id).update(is_active=False)
    resume.is_active = True
    resume.save()

    return Response({'msg': '启用成功'})


# ========== 删除简历 ==========
@api_view(['DELETE', 'POST'])
def delete_resume(request, resume_id):
    try:
        resume = Resume.objects.get(id=resume_id)
    except Resume.DoesNotExist:
        return Response({'msg': '简历不存在'}, status=status.HTTP_404_NOT_FOUND)

    user_id = resume.user_id
    was_active = resume.is_active
    resume.delete()

    if was_active:
        next_resume = Resume.objects.filter(user_id=user_id).order_by('-updated_at', '-created_at').first()
        if next_resume:
            next_resume.is_active = True
            next_resume.save()

    return Response({'msg': '删除成功'})


# ========== 投递职位 ==========
@api_view(['POST'])
def apply_job(request):
    data = request.data.copy()

    if not data.get('resume') and data.get('user'):
      active_resume = Resume.objects.filter(user_id=data.get('user'), is_active=True).first()
      if active_resume:
          data['resume'] = active_resume.id

    serializer = ApplicationSerializer(data=data)
    if serializer.is_valid():
        serializer.save()
        return Response({'msg': '投递成功'}, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ========== 推荐职位 ==========
@api_view(['GET'])
def recommend_jobs(request):
    user_id = request.query_params.get('user_id')
    if not user_id:
        return Response({'msg': '缺少 user_id'}, status=status.HTTP_400_BAD_REQUEST)

    resume = Resume.objects.filter(user_id=user_id, is_active=True).first()
    if not resume:
        return Response({'msg': '请先选择一份启用简历'}, status=status.HTTP_400_BAD_REQUEST)

    from .recommender import get_recommendations
    ranked = get_recommendations(resume)

    if not ranked:
        return Response([])

    result = []
    for job, score in ranked:
        job_data = JobSerializer(job).data
        job_data['score'] = round(float(score), 4)
        result.append(job_data)

    return Response(result)


# ========== 我的投递记录 ==========
@api_view(['GET'])
def my_applications(request):
    user_id = request.query_params.get('user_id')
    apps = Application.objects.filter(user_id=user_id).order_by('-apply_time')
    serializer = ApplicationSerializer(apps, many=True)
    return Response(serializer.data)


# ========== HR的职位列表 ==========
@api_view(['GET'])
def my_jobs(request):
    hr_id = request.query_params.get('hr_id')
    jobs = Job.objects.filter(hr_id=hr_id)
    serializer = JobSerializer(jobs, many=True)
    return Response(serializer.data)


# ========== HR查看某职位候选人 ==========
from .models import Application, Job
from .serializers import ApplicationSerializer
from .recommender import tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def calc_resume_job_score(resume, job):
    if not resume or not job:
        return 0

    resume_text = " ".join([
        resume.skills or "",
        resume.expect_job or "",
        resume.work_exp or "",
        resume.self_intro or "",
        resume.education_exp or "",
        getattr(resume, "project_exp", "") or "",
        getattr(resume, "certificate_exp", "") or "",
        resume.major or "",
        resume.degree or "",
        resume.expect_city or "",
    ])

    job_text = " ".join([
        job.title or "",
        job.description or "",
        job.skill_required or "",
        job.city or "",
        job.degree_required or "",
        job.exp_required or "",
        job.job_type or "",
    ])

    resume_text = tokenize(resume_text)
    job_text = tokenize(job_text)

    corpus = [resume_text, job_text]
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)
    score = cosine_similarity(tfidf_matrix[0], tfidf_matrix[1])[0][0]

    return round(float(score) * 100, 1)


@api_view(['GET'])
def job_candidates(request, job_id):
    apps = Application.objects.filter(job_id=job_id).select_related('user', 'resume', 'job', 'job__company')
    serializer = ApplicationSerializer(apps, many=True)
    data = serializer.data

    try:
        job = Job.objects.get(id=job_id)
    except Job.DoesNotExist:
        return Response({'msg': '职位不存在'}, status=404)

    for i, app in enumerate(apps):
        data[i]['match_score'] = calc_resume_job_score(app.resume, job)

    return Response(data)


# ========== HR更新候选人状态 ==========
@api_view(['POST'])
def update_application_status(request, app_id):
    try:
        app = Application.objects.get(id=app_id)
        app.status = request.data.get('status')
        app.save()
        return Response({'msg': '状态更新成功'})
    except Application.DoesNotExist:
        return Response({'msg': '记录不存在'}, status=status.HTTP_404_NOT_FOUND)


# ========== 用户列表（管理员） ==========
@api_view(['GET'])
def user_list(request):
    users = User.objects.all()
    serializer = UserListSerializer(users, many=True)
    return Response(serializer.data)


# ========== 封禁/解封用户 ==========
@api_view(['POST'])
def toggle_user(request, user_id):
    try:
        user = User.objects.get(id=user_id)
        user.is_active = not user.is_active
        user.save()
        return Response({'msg': '操作成功'})
    except User.DoesNotExist:
        return Response({'msg': '用户不存在'}, status=status.HTTP_404_NOT_FOUND)


# ========== 待审核职位列表 ==========
@api_view(['GET'])
def pending_jobs(request):
    jobs = Job.objects.filter(status='pending')
    serializer = JobSerializer(jobs, many=True)
    return Response(serializer.data)


# ========== 审核职位 ==========
@api_view(['POST'])
def review_job(request, job_id):
    try:
        job = Job.objects.get(id=job_id)
        job.status = request.data.get('status')
        job.save()
        return Response({'msg': '审核完成'})
    except Job.DoesNotExist:
        return Response({'msg': '职位不存在'}, status=status.HTTP_404_NOT_FOUND)


# ========== 平台统计 ==========
@api_view(['GET'])
def stats(request):
    return Response({
        'users': User.objects.count(),
        'jobs': Job.objects.count(),
        'resumes': Resume.objects.count(),
        'applications': Application.objects.count(),
    })