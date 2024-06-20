<template>
  <div>
    <div class="top-bar">
      <div class="left">
        <span>ChatWithAIs V1 | 一站式大语言模型访问平台</span>
      </div>
      <div class="right">
        <button @click="goBack" class="home-link">返回</button>
      </div>
    </div>

    <div class="info-heading">
      <h2>用户信息</h2>
    </div>

    <div v-if="users.length > 0" class="user-container">
      <ul>
        <li v-for="user in users" :key="user.id" class="user-item">
          <p><strong>用户编号：</strong> {{ user.id }}</p>
          <p><strong>用户名：</strong> {{ user.username }}</p>
          <p><strong>是否为管理员：</strong> {{ user.is_admin ? '是' : '否' }}</p>
          <!-- 其他用户信息 -->
        </li>
      </ul>
    </div>
    <div v-else>
      <p>暂无用户信息。</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import router from "@/router";
axios.defaults.withCredentials = true;
export default {
  name: 'UserInformation',
  data() {
    return {
      users: []
    };
  },
  async created() {
    await this.fetchUsers();
  },
  methods: {
    async fetchUsers() {
      try {
        const response = await axios.get('/api/admin/users', { withCredentials: true });
        this.users = response.data.users;
      } catch (error) {
        console.error('获取用户信息失败：', error);
      }
    },
    goBack() {
      router.push({ name: 'AdminDashboard' });
    }
  }
};
</script>

<style scoped>
.info-heading {
  text-align: center;
  margin-bottom: 20px;
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

.top-bar .right button {
  margin-left: 0px;
  padding: 8px 16px;
  background-color: #ffffff;
  color: #1296db;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s;
  font-weight: bold;
  border: none;
  font-size: 15px;
}

.top-bar .right button:hover {
  background-color: #1296db;
  color: #ffffff;
}

.user-container {
  margin-top: 20px;
  max-height: 700px;
  overflow-y: auto;
}

.user-item {
  margin-bottom: 20px;
  padding: 15px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background-color: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.user-item p {
  margin: 5px 0;
}

.user-item p strong {
  font-weight: bold;
}
</style>
