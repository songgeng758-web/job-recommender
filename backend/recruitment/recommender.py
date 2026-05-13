import jieba
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from .models import Job


def tokenize(text):
    """中文分词"""
    text = text or ""
    return " ".join(jieba.cut(text))


def build_resume_text(resume):
    """把简历字段拼接成推荐文本"""
    parts = [
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
    ]
    return tokenize(" ".join(parts))


def build_job_text(job):
    """把职位字段拼接成推荐文本"""
    parts = [
        job.title or "",
        job.description or "",
        job.skill_required or "",
        job.city or "",
        job.degree_required or "",
        job.exp_required or "",
        job.job_type or "",
    ]
    return tokenize(" ".join(parts))


def get_recommendations(resume):
    """
    根据简历推荐职位
    resume: Resume 对象
    返回: [(job对象, 相似度分数), ...]
    """
    if not resume:
        return []

    resume_text = build_resume_text(resume)

    jobs = list(Job.objects.filter(status='approved'))
    if not jobs:
        return []

    job_texts = [build_job_text(job) for job in jobs]

    corpus = [resume_text] + job_texts
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)

    resume_vec = tfidf_matrix[0]
    job_vecs = tfidf_matrix[1:]
    scores = cosine_similarity(resume_vec, job_vecs)[0]

    ranked = sorted(zip(jobs, scores), key=lambda x: x[1], reverse=True)
    return ranked