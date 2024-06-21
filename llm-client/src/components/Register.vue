<template>
  <div>
    <!-- 顶部栏 -->
    <div class="top-bar">
      <div class="left">
        <span>ChatWithAIs V2 | 一站式大语言模型访问平台</span>
      </div>
    </div>

    <div class="register-page">
      <div class="register-container">
        <h2 class="register-title">注册新账号</h2>
        <form @submit.prevent="register" class="register-form">
          <div class="form-group">
            <label for="username">用户名：</label>
            <input type="text" v-model="username" class="input-field" required>
          </div>
          <div class="form-group">
            <label for="password">密码：</label>
            <input type="password" v-model="password" class="input-field" required>
          </div>
          <div class="form-group">
            <label for="email">邮箱：</label>
            <div class="input-with-button">
              <input type="email" v-model="email" class="input-field" required>
              <button type="button" :disabled="isSendingCode" @click="sendAuthCode" class="auth-code-button">
                {{ sendButtonText }}
              </button>
            </div>
          </div>
          <div class="form-group">
            <label for="authcode">验证码：</label>
            <input type="text" v-model="authcode" class="input-field" required>
          </div>
          <button type="submit" class="register-button">注册</button>
        </form>
        <p class="register-message">{{ message }}</p>
        <p>已有账号？ <router-link to="/login">点击这里登录</router-link></p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
axios.defaults.withCredentials = true;
export default {
  name: 'RegisterComponent',
  data() {
    return {
      username: '',
      password: '',
      email: '',
      authcode: '',
      message: '',
      isSendingCode: false,
      countdown: 60,
      timer: null
    };
  },
  computed: {
    sendButtonText() {
      return this.isSendingCode ? `重新发送(${this.countdown}s)` : '发送验证码';
    }
  },
  methods: {
    async sendAuthCode() {
      try {
        this.isSendingCode = true;
        this.countdown = 60;
        this.startCountdown();

        const response = await axios.post('/api/authenticate', {
          username: this.username,
          email: this.email
        });
        this.message = response.data.message;
      } catch (error) {
        this.message = error.response && error.response.data ? error.response.data.message : '验证码发送失败，请稍后重试。';
        this.isSendingCode = false;
        clearInterval(this.timer);
      }
    },
    startCountdown() {
      this.timer = setInterval(() => {
        if (this.countdown > 0) {
          this.countdown--;
        } else {
          this.isSendingCode = false;
          clearInterval(this.timer);
        }
      }, 1000);
    },
    async register() {
      try {
        const response = await axios.post('/api/register', {
          username: this.username,
          password: this.password,
          email: this.email,
          authcode: this.authcode
        });
        this.message = response.data.message;
        if (response.status === 201) {
          this.message += ' 2s后自动跳转到登录页面...';
          setTimeout(() => {
            this.$router.push('/login');
          }, 2000); // 2秒后重定向到登录页面
        }
      } catch (error) {
        this.message = error.response && error.response.data ? error.response.data.message : '注册失败，请稍后重试。';
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

/* 注册页面样式 */
.register-page {
  background-image: url('@/assets/homepage0.png');
  background-size: cover;
  background-position: center;
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
}

.register-container {
  max-width: 400px;
  width: 100%;
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  text-align: center;
  margin-top: -60px;
}

.register-title {
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
  flex: 0.93;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.1);
  transition: box-shadow 0.3s ease;
}

.input-with-button {
  display: flex;
  align-items: center;
}

.input-field:focus {
  outline: none;
  box-shadow: 0 0 5px rgba(0, 0, 0, 0.3);
}

.auth-code-button {
  margin-left: 10px;
  background-color: #007bff;
  color: #fff;
  width: 105px;
  padding: 10px 10px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  white-space: nowrap;  /* 防止按钮文字换行 */
}

.auth-code-button:disabled {
  background-color: #6c757d;
  cursor: not-allowed;
}

.auth-code-button:hover:enabled {
  background-color: #0056b3;
}

.register-button {
  background-color: #28a745;
  color: #fff;
  padding: 12px 24px;
  border: none;
  border-radius: 5px;
  font-size: 18px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.register-button:hover {
  background-color: #218838;
}

.register-message {
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
