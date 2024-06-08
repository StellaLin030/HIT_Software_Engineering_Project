<template>
  <div class="logout-container">
    <h2>Logging out...</h2>
    <p>{{ logoutMessage }}</p>
  </div>
</template>

<script>
import axios from 'axios';
import router from '../router';

export default {
  name: 'LogoutComponent',
  data() {
    return {
      logoutMessage: ''
    };
  },
  async created() {
    await this.logout();
  },
  methods: {
    async logout() {
      try {
        const response = await axios.get('/api/logout', { withCredentials: true });
        if (response.data.status === 'success') {
          this.logoutMessage = response.data.message;
          setTimeout(() => {
            router.push({ name: 'HomeView' });
            this.logoutMessage = '';
          }, 1500);
        } else {
          this.logoutMessage = response.data.message;
        }
      } catch (error) {
        console.error('Logout request failed:', error);
        this.logoutMessage = '登出失败，请检查您的网络连接或重试。';
      }
    }
  }
};
</script>

<style scoped>
.logout-container {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  text-align: center;
}
</style>
