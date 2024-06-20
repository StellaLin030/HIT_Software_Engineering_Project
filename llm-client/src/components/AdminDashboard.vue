<template>
  <div class="admin-dashboard-background">
    <!-- 顶部栏 -->
    <div class="top-bar">
      <div class="left">
        <span>ChatWithAIs V1 | 一站式大语言模型访问平台</span>
      </div>
      <div class="right">
        <button @click="logout" class="logout-button">登出</button>
      </div>
    </div>

    <!-- 功能容器 -->
    <div class="dashboard-container">
      <h2>管理员仪表板</h2>
      <div class="function-buttons">
        <button @click="goToFeedback" class="dashboard-button">查看反馈信息</button>
        <button @click="goToUserInformation" class="dashboard-button">查看用户信息</button>
      </div>
      <p>{{ logoutMessage }}</p>
    </div>
  </div>
</template>

<script>
import router from '../router';

export default {
  name: 'AdminDashboard',
  data() {
    return {
      logoutMessage: ''
    };
  },
  methods: {
    logout() {
      router.push({ name: 'Logout' });
    },
    goToFeedback() {
      router.push({ name: 'AdminFeedback' });
    },
    goToUserInformation() {
      router.push({ name: 'AdminUserInfo' });
    }
  }
};
</script>

<style scoped>
.admin-dashboard-background {
  background-image: url('@/assets/feedback.png');
  background-size: cover;
  background-position: center;
  height: 100vh;
}

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

.top-bar .right .logout-button {
  margin-left: 15px;
  padding: 8px 16px;
  background-color: #ffffff;
  color: #1296db;
  border-radius: 5px;
  text-decoration: none;
  transition: background-color 0.3s, color 0.3s;
  font-weight: bold;
  border: none;
  font-size: 15px;
}

.top-bar .right .logout-button:hover {
  background-color: #1296db;
  color: #ffffff;
}

.dashboard-container {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
  background-color: #fff;
  padding: 20px;
  border-radius: 10px;
}

.function-buttons {
  margin-top: 20px;
}

.dashboard-button {
  margin: 10px;
  padding: 10px 20px;
  background-color: #1296db;
  color: #fff;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.dashboard-button:hover {
  background-color: #0056b3;
}
</style>
