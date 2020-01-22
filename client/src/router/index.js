import Vue from 'vue';
import VueRouter from 'vue-router';
import Search from '@/components/Search.vue';
import Login from '@/components/Login.vue';
import Logout from '@/components/Logout.vue';
import Register from '@/components/Register.vue';
import Profile from '@/components/Profile.vue';
import Giphy from '@/components/Giphy.vue';

Vue.use(VueRouter);

const routes = [
  {
    path: '/search',
    name: 'Search',
    component: Search,
  },
  {
    path: '/giphy/:giphyId',
    name: 'Giphy',
    component: Giphy,
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/logout',
    name: 'Logout',
    component: Logout,
  },
  {
    path: '/register',
    name: 'Register',
    component: Register,
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    meta: {
      requiresAuth: true,
    },
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.VUE_APP_BASE_URL,
  routes,
});

export default router;
