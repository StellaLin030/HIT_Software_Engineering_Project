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

    <div class="feedback-heading">
      <h2>用户反馈信息</h2>
    </div>

    <div v-if="feedbacks.length > 0" class="feedback-container">
      <ul>
        <li v-for="feedback in feedbacks" :key="feedback.id" class="feedback-item">
          <p><strong>反馈编号：</strong> {{ feedback.id }}</p>
          <p><strong>用户编号：</strong> {{ feedback.user_id }}</p>
          <p><strong>用户名：</strong> {{ feedback.username }}</p>
          <p><strong>消息：</strong> {{ feedback.message }}</p>
          <p><strong>时间戳：</strong> {{ new Date(feedback.timestamp).toLocaleString() }}</p>
        </li>
      </ul>
    </div>
    <div v-else>
      <p>暂无反馈。</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import router from "@/router";

export default {
  name: 'AdminFeedback',
  data() {
    return {
      feedbacks: []
    };
  },
  async created() {
    await this.fetchFeedbacks();
  },
  methods: {
    async fetchFeedbacks() {
      try {
        const response = await axios.get('/api/admin/feedback', { withCredentials: true });
        this.feedbacks = response.data.feedbacks;
      } catch (error) {
        console.error('获取反馈信息时出错：', error);
      }
    },
    goBack() {
      // 返回到之前的对话页面的逻辑
      router.push({ name: 'AdminDashboard' });
    }
  }
};
</script>

<style scoped>
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

.feedback-container {
  max-height: 700px;
  overflow-y: auto;
}

.feedback-heading {
  text-align: center;
  margin-bottom: 20px;
}

.feedback-item {
  margin-bottom: 20px;
  padding: 15px;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  background-color: #ffffff;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.feedback-item p {
  margin: 5px 0;
}

.feedback-item p strong {
  font-weight: bold;
}

.feedback-item p:last-child {
  margin-bottom: 0;
}
</style>
