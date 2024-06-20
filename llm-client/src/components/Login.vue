<template>
  <div>
    <!-- 顶部栏 -->
    <div class="top-bar">
      <div class="left">
        <span>ChatWithAIs V1 | 一站式大语言模型访问平台</span>
      </div>
    </div>

    <div class="login-page">
      <div class="login-container">
        <h2 class="login-title">欢迎回来！</h2>
        <form @submit.prevent="login" class="login-form">
          <div class="form-group">
            <label for="username">用户名：</label>
            <input type="text" v-model="username" class="input-field" required>
          </div>
          <div class="form-group">
            <label for="password">密码：</label>
            <input type="password" v-model="password" class="input-field" required>
          </div>
          <button type="submit" class="login-button">登录</button>
        </form>
        <p class="login-message">{{ message }}</p>
        <p>还没有账号？ <router-link to="/register">点击这里注册</router-link></p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
axios.defaults.withCredentials = true;
import router from '@/router/index.js';

export default {
  name: 'Login',
  data() {
    return {
      username: '',
      password: '',
      message: ''
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post('/api/login', {
          username: this.username,
          password: this.password
        }, { withCredentials: true });
        this.message = response.data.message;
        if (response.data.role === 'admin') {
          router.push({ name: 'AdminDashboard' });
        } else {
          router.push({ name: 'UserDashboard' });
        }
      } catch (error) {
        this.message = error.response && error.response.data ? error.response.data.message : '登录失败，请稍后重试。';
      }
    }
  }
};
</script>

<style scoped>
/* 顶部栏样式 */
.top-bar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #D6EAF8;
  padding: 10px;
  color: #1296db;
  height: 35px;
  font-weight: bold;
}

.top-bar .left {
  font-size: 20px;
}

.top-bar .right .home-link {
  margin-left: 15px;
  padding: 10px 20px;
  background-color: #ffffff;
  color: #1296db;
  border-radius: 5px;
  text-decoration: none;
  transition: background-color 0.3s, color 0.3s;
  font-weight: bold;
}

.top-bar .right .home-link:hover {
  background-color: #1296db;
  color: #ffffff;
}

/* 登录页面样式 */
.login-page {
  background-image: url('@/assets/homepage0.png');
  background-size: cover;
  background-position: center;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.login-container {
  max-width: 400px;
  width: 100%;
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  text-align: center;
  margin-top: -60px;
}

.login-title {
  margin-bottom: 30px;
  font-size: 28px;
  font-weight: 600;
}

.form-group {
  margin-bottom: 20px;
  display: flex;
  align-items: center;
}

.form-group label {
  width: 80px;
}

.input-field {
  width: 250px;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
}

.input-field:focus {
  outline: none;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);
}

.login-button {
  background-color: #1296db;
  color: #fff;
  padding: 12px 24px;
  border: none;
  border-radius: 5px;
  font-size: 18px;
  font-weight: 600;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.login-button:hover {
  background-color: #0056b3;
}

.login-message {
  margin-top: 20px;
  font-size: 16px;
  color: #ff0000;
}

a {
  color: #007bff;
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
</style>
