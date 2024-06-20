<template>
  <div class="feedback-background">
    <!-- 顶部栏 -->
    <div class="top-bar">
      <div class="left">
        <span>ChatWithAIs V1 | 一站式大语言模型访问平台</span>
      </div>
      <div class="right">
        <button @click="goBack" class="home-link">返回</button>
      </div>
    </div>

    <div class="feedback-container">
      <div class="feedback-form">
        <h2>用户反馈</h2>
        <form @submit.prevent="submitFeedback">
          <textarea v-model="feedback" placeholder="请输入您的反馈..." required></textarea>
          <button type="submit">提交反馈</button>
        </form>
        <p>{{ feedbackMessage }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import router from "@/router";
axios.defaults.withCredentials = true;
export default {
  name: 'Feedback',
  data() {
    return {
      feedback: '',
      feedbackMessage: ''
    };
  },
  methods: {
    async submitFeedback() {
      try {
        await axios.post('/api/user/feedback', {
          message: this.feedback // 使用正确的字段名
        },{ withCredentials: true });
        this.feedbackMessage = '反馈提交成功！感谢您的反馈。';
        this.feedback = ''; // 清空反馈
      } catch (error) {
        this.feedbackMessage = '反馈提交失败，请稍后重试。';
        console.error('Feedback submission error:', error);
      }
    },
    goBack() {
      // 返回到之前的对话页面的逻辑
      router.push({ name: 'UserDashboard' });
    }
  }
};
</script>

<style scoped>
.feedback-background {
  background-image: url('@/assets/feedback.png');
  background-size: cover;
  background-position: center;
  height: 100vh;
  display: flex;
  flex-direction: column;
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
}

.top-bar .right button:hover {
  background-color: #1296db;
  color: #ffffff;
}

.feedback-container {
  flex: 1;
  display: flex;
  justify-content: center;
  align-items: center;
}

.feedback-form {
  width: 400px;
  max-width: 90%;
  background-color: rgba(255, 255, 255, 0.9);
  padding: 20px;
  border-radius: 10px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

.feedback-form h2 {
  margin-bottom: 20px;
  text-align: center;
}

textarea {
  width: calc(100% - 40px);
  height: 150px;
  margin: 0 auto 20px auto;
  padding: 10px;
  border: 1px solid #ccc;
  border-radius: 5px;
  resize: vertical;
  display: block;
}

button {
  width: 100%;
  padding: 10px;
  background-color: #1296db;
  color: #fff;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

button:hover {
  background-color: #0056b3;
}

.feedback-form p {
  margin-top: 10px;
  font-size: 14px;
  color: #ff0000;
}
</style>
