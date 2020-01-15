import Vue from 'vue';
import VueRouter from 'vue-router';
import Home from '@/components/Home.vue';
import Save from '@/components/Save.vue';
import Results from '@/components/Results.vue';
import Login from '@/components/Login.vue';
import Profile from '@/components/Profile.vue';
import store from '@/store';

Vue.use(VueRouter);

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/save/:id',
    name: 'Save',
    component: Save,
    beforeEnter(to, from, next) {
      if (!store.getters.isAuthenticated) {
        next('/login');
      } else {
        next();
      }
    },
  },
  {
    path: '/profile',
    name: 'Profile',
    component: Profile,
    beforeEnter(to, from, next) {
      if (!store.getters.isAuthenticated) {
        next('/login');
      } else {
        next();
      }
    },
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/results',
    name: 'Results',
    component: Results,
  },
];

const router = new VueRouter({
  mode: 'history',
  base: process.env.VUE_APP_BASE_URL,
  routes,
});

export default router;
