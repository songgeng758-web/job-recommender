<template>
  <div class="register-container">
    <el-card class="register-card">
      <h2 style="text-align:center;margin-bottom:24px">注册账号</h2>
      <el-form :model="form" label-width="80px">
        <el-form-item label="用户名">
          <el-input v-model="form.username" placeholder="请输入用户名" />
        </el-form-item>
        <el-form-item label="密码">
          <el-input v-model="form.password" type="password" placeholder="请输入密码" />
        </el-form-item>
        <el-form-item label="手机号">
          <el-input v-model="form.phone" placeholder="请输入手机号" />
        </el-form-item>
        <el-form-item label="邮箱">
          <el-input v-model="form.email" placeholder="请输入邮箱" />
        </el-form-item>
        <el-form-item label="角色">
          <el-select v-model="form.role" style="width:100%">
            <el-option label="求职者" value="seeker" />
            <el-option label="企业HR" value="hr" />
            <el-option label="管理员" value="admin" />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" style="width:100%" @click="handleRegister">注册</el-button>
        </el-form-item>
        <el-form-item>
          <el-button style="width:100%" @click="$router.push('/')">已有账号？去登录</el-button>
        </el-form-item>
      </el-form>
    </el-card>
  </div>
</template>

<script setup>
import { reactive } from 'vue'
import { useRouter } from 'vue-router'
import axios from 'axios'
import { ElMessage } from 'element-plus'

const router = useRouter()
const form = reactive({ username: '', password: '', phone: '', email: '', role: 'seeker' })

const handleRegister = async () => {
  try {
    await axios.post('http://127.0.0.1:8000/api/users/register/', form)
    ElMessage.success('注册成功，请登录')
    router.push('/')
  } catch (e) {
    ElMessage.error('注册失败，用户名可能已存在')
  }
}
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: #f0f2f5;
}
.register-card {
  width: 400px;
}
</style>