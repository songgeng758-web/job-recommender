from rest_framework import serializers
from .models import User, Resume, Job, Application, Company
import hashlib


class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'password', 'role', 'phone', 'email']

    def create(self, validated_data):
        # 密码加密存储
        validated_data['password'] = hashlib.md5(
            validated_data['password'].encode()
        ).hexdigest()
        return super().create(validated_data)


class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()


class JobSerializer(serializers.ModelSerializer):
    company_name = serializers.SerializerMethodField()

    class Meta:
        model = Job
        fields = '__all__'

    def get_company_name(self, obj):
        if obj.company:
            return obj.company.company_name
        return None


class ResumeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Resume
        fields = '__all__'


class ApplicationSerializer(serializers.ModelSerializer):
    job_title = serializers.CharField(source='job.title', read_only=True)
    company_name = serializers.SerializerMethodField()
    city = serializers.CharField(source='job.city', read_only=True)
    salary_min = serializers.IntegerField(source='job.salary_min', read_only=True)
    salary_max = serializers.IntegerField(source='job.salary_max', read_only=True)

    candidate_name = serializers.SerializerMethodField()
    candidate_username = serializers.CharField(source='user.username', read_only=True)
    school = serializers.CharField(source='resume.school', read_only=True)
    major = serializers.CharField(source='resume.major', read_only=True)
    degree = serializers.CharField(source='resume.degree', read_only=True)
    expect_job = serializers.CharField(source='resume.expect_job', read_only=True)
    resume_title = serializers.CharField(source='resume.title', read_only=True)

    class Meta:
        model = Application
        fields = [
            'id',
            'job',
            'user',
            'resume',
            'status',
            'apply_time',

            'job_title',
            'company_name',
            'city',
            'salary_min',
            'salary_max',

            'candidate_name',
            'candidate_username',
            'school',
            'major',
            'degree',
            'expect_job',
            'resume_title',
        ]

    def get_company_name(self, obj):
        if obj.job and obj.job.company:
            return obj.job.company.company_name
        return None

    def get_candidate_name(self, obj):
        if obj.resume and obj.resume.real_name:
            return obj.resume.real_name
        if obj.user:
            return obj.user.username
        return '未知候选人'


class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'


class UserListSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'role', 'phone', 'email', 'is_active']