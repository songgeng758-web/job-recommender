<template>
  <div class="login-wrapper">
    <div class="login-left">
      <div class="brand">
        <div class="logo">🎯 智聘平台</div>
        <h1>高效直达 · 智能匹配</h1>
        <p>基于内容推荐的智能求职招聘系统，连接 1,000,000+ 优质岗位。</p>
        <div class="features">
          <div class="feature-item">✨ AI智能匹配，精准推荐职位</div>
          <div class="feature-item">🏢 海量企业，优质岗位</div>
          <div class="feature-item">🚀 简历一键投递，高效求职</div>
        </div>
      </div>
    </div>
    <div class="login-right">
      <div class="login-box">
        <h2>欢迎回来</h2>
        <p class="subtitle">登录你的账号，开启职业新篇章</p>
        <el-form :model="form" size="large">
          <el-form-item>
            <el-input v-model="form.username" placeholder="请输入用户名"
              prefix-icon="User" clearable />
          </el-form-item>
          <el-form-item>
            <el-input v-model="form.password" type="password" placeholder="请输入密码"
              prefix-icon="Lock" show-password />
          </el-form-item>
          <el-form-item>
            <el-button type="primary" style="width:100%;height:48px;font-size:16px;border-radius:8px"
              :loading="loading" @click="handleLogin">立即登录</el-button>
          </el-form-item>
        </el-form>
        <div class="register-tip">
          还没有账号？<el-link type="primary" @click="$router.push('/register')">立即注册</el-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const router = useRouter()
const form = reactive({ username: '', password: '' })
const loading = ref(false)

const handleLogin = async () => {
  if (!form.username || !form.password) {
    ElMessage.warning('请填写用户名和密码')
    return
  }
  loading.value = true
  try {
    const res = await axios.post('http://127.0.0.1:8000/api/users/login/', form)
    localStorage.setItem('user_id', res.data.user_id)
    localStorage.setItem('username', res.data.username)
    localStorage.setItem('role', res.data.role)
    ElMessage.success('登录成功')
    const role = res.data.role
    if (role === 'seeker') router.push('/seeker')
    else if (role === 'hr') router.push('/hr')
    else if (role === 'admin') router.push('/admin')
  } catch (e) {
    ElMessage.error('用户名或密码错误')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
* { box-sizing: border-box; margin: 0; padding: 0; }

.login-wrapper {
  display: flex;
  height: 100vh;
  width: 100vw;
  overflow: hidden;
}

.login-left {
  flex: 1;
  background: linear-gradient(135deg, #1565c0 0%, #1a237e 100%);
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 60px;
}

.brand {
  color: white;
  max-width: 480px;
}

.logo {
  font-size: 22px;
  font-weight: bold;
  margin-bottom: 40px;
  opacity: 0.95;
}

.brand h1 {
  font-size: 38px;
  font-weight: bold;
  line-height: 1.3;
  margin-bottom: 20px;
}

.brand p {
  font-size: 15px;
  opacity: 0.8;
  line-height: 1.7;
  margin-bottom: 48px;
}

.features {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.feature-item {
  font-size: 15px;
  opacity: 0.9;
  display: flex;
  align-items: center;
  gap: 8px;
  background: rgba(255,255,255,0.1);
  padding: 12px 20px;
  border-radius: 8px;
}

.login-right {
  width: 500px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: #fff;
  padding: 60px 50px;
  box-shadow: -4px 0 30px rgba(0,0,0,0.08);
}

.login-box {
  width: 100%;
}

.login-box h2 {
  font-size: 30px;
  font-weight: bold;
  color: #1a1a1a;
  margin-bottom: 8px;
}

.subtitle {
  color: #999;
  font-size: 14px;
  margin-bottom: 36px;
}

.register-tip {
  text-align: center;
  color: #999;
  font-size: 14px;
  margin-top: 20px;
}
</style>