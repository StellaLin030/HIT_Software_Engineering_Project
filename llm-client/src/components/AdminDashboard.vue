<template>
  <div class="admin-dashboard-background">
    <!-- 顶部栏 -->
    <div class="top-bar">
      <div class="left">
        <span>ChatWithAIs V2 | 一站式大语言模型访问平台</span>
      </div>
      <div class="right">
        <button @click="logout" class="logout-button">登出</button>
      </div>
    </div>

    <!-- 统计信息 -->
    <div class="dashboard-container">
      <h2>管理员仪表板</h2>
      <div class="overall-situation">
        <el-row :gutter="20">
          <el-col :span="6">
            <div>
              <el-statistic
                  group-separator=","
                  :precision="0"
                  :value="value2"
                  :title="title2"
              >
                <template slot="suffix">
                <span @click="goToUserInformation" class="like">
                  <i
                      class="el-icon-view"
                      style="color:red"
                  ></i>
                </span>
                </template>
              </el-statistic>
            </div>
          </el-col>
          <el-col :span="6">
            <div>
              <el-statistic
                  group-separator=","
                  :precision="0"
                  decimal-separator="."
                  :value="value1"
                  :title="title1"
              >
                <template slot="prefix">
                  <i @click="goToCreaseUserInfo" class="el-icon-s-flag" style="color: red"></i>
                </template>
                <template slot="suffix">
                  <i @click="goToCreaseUserInfo" class="el-icon-s-flag" style="color: blue"></i>
                </template>
              </el-statistic>
            </div>
          </el-col>
          <el-col :span="6">
            <div>
              <el-statistic :value=unread_feedback title="未读反馈">
                <template slot="suffix">
                <span @click="goToUnreadFeedback" class="like">
                  <i
                      class="el-icon-view"
                      style="color:red"
                  ></i>
                </span>
                </template>
              </el-statistic>
            </div>
          </el-col>
          <el-col :span="6">
            <div>
              <el-statistic
                  group-separator=","
                  :precision="0"
                  :value="value3"
                  :title="title3"
              >
                <template slot="suffix">
                <span @click="goToFeedback" class="like">
                  <i
                      class="el-icon-view"
                      style="color:red"
                  ></i>
                </span>
                </template>
              </el-statistic>
            </div>
          </el-col>
        </el-row>
        <p>{{ logoutMessage }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import router from "@/router";

export default {
  name: 'AdminDashboard',
  data() {
    return {
      like: true,
      value1: null,
      value2: null,
      value3: null,
      title1: "增长人数(较上月的今天)",
      title2: "总人数",
      title3: "总反馈数",
      unread_feedback:null,
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
    },
    goToCreaseUserInfo() {
      router.push({ name: 'UserCreaseInfo' });
    },
    goToUnreadFeedback() {
      router.push({ name: 'AdminUnreadFeedback' });
    },
    // 获取总人数
    fetchUserCount() {
      axios.get('/api/admin/number_user', { withCredentials: true })
          .then(response => {
            this.value2 = response.data.total_users;
          })
          .catch(error => {
            console.error("There was an error fetching the user count:", error);
          });
    },
    // 获取增长人数
    fetchIncreaseUserCount() {
      axios.get('/api/admin/increase_user', { withCredentials: true })
          .then(response => {
            this.value1 = response.data.increase_users;
          })
          .catch(error => {
            console.error("There was an error fetching the increase user count:", error);
          });
    },
    // 获取未读反馈数量
    fetchUnreadFeedbackCount() {
      axios.get('/api/admin/number_unreadfeedback', { withCredentials: true })
          .then(response => {
            this.unread_feedback = response.data.unread_feedback;
          })
          .catch(error => {
            console.error("There was an error fetching the unread feedback count:", error);
          });
    },
    // 获取未读反馈数量
    fetchAllFeedbackCount() {
      axios.get('/api/admin/number_allfeedback', { withCredentials: true })
          .then(response => {
            this.value3 = response.data.allfeedback;
          })
          .catch(error => {
            console.error("There was an error fetching the all feedback count:", error);
          });
    },
  },

  // 钩子 处于该界面自动获取
  created() {
    this.fetchUserCount();
    this.fetchIncreaseUserCount();
    this.fetchUnreadFeedbackCount();
    this.fetchAllFeedbackCount();
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
  width: 80%;
  height: 20%;
}

.overall-situation{
  margin-top: 40px;
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

.like {
  cursor: pointer !important;
  font-size: 25px;
  display: inline-block;
}

</style>
