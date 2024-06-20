import Vue from 'vue'
import VueRouter from 'vue-router'
import HomeView from '../views/HomeView.vue';
import Login from '../components/Login.vue';
import Register from '../components/Register.vue';
import UserDashboard from '../components/UserDashboard.vue';
import AdminDashboard from '../components/AdminDashboard.vue';
import Logout from '../components/Logout.vue';
import Feedback from '../components/Feedback.vue'; // 将FeedbackForm改为FeedbackComponent
import AdminFeedback from '../components/AdminFeedback.vue';
import AdminUserInfo from '../components/UserInformation.vue';

Vue.use(VueRouter)

const routes = [
  { path: '/', name: 'HomeView', component: HomeView },
  { path: '/login', name: 'Login', component: Login },
  { path: '/register', name: 'Register', component: Register },
  { path: '/user-dashboard', name: 'UserDashboard', component: UserDashboard, meta: { requiresAuth: true, role: 'user' } },
  { path: '/admin-dashboard', name: 'AdminDashboard', component: AdminDashboard, meta: { requiresAuth: true, role: 'admin' } },
  { path: '/logout', name: 'Logout', component: Logout },
  { path: '/feedback', name: 'Feedback', component: Feedback }, // 这里改为FeedbackComponent
  { path: '/admin-feedback', name: 'AdminFeedback', component: AdminFeedback },
  { path: '/admin-userinfo', name: 'AdminUserInfo', component: AdminUserInfo },
]

const router = new VueRouter({
  routes
})

export default router
