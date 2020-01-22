import Vue from 'vue';
import VueCookies from 'vue-cookies';
import VueLodash from 'vue-lodash';
import App from '@/App.vue';
import router from '@/router';
import store from '@/store';

Vue.config.productionTip = false;
// eslint-disable-next-line
Vue.prototype.$log = console.log;
Vue.use(VueCookies);
Vue.use(VueLodash);

new Vue({
  router,
  store,
  render: h => h(App),
}).$mount('#app');
