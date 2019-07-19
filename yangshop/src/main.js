import Vue from 'vue'
import App from './App.vue'
import router from './router'
import store from './store'
import VueResource from 'vue-resource'
Vue.config.productionTip = false
Vue.use(VueResource)
Vue.http.options.emulateJSON = false;
Vue.http.options.root = 'http://api.shop.yanggebook.xyz';
import { Toast } from 'vant';
import 'vant/lib/icon/local.css';

Vue.use(Toast);

Vue.http.interceptors.push((request, next) => {
  if (store.state.userInfo.token) {
    request.headers.set('Authorization', `JWT ${store.state.userInfo.token}`);
  }
  next((response) => {
    if (response.status === 401) {
      if (response.body.detail == '身份认证信息未提供。') {
        Toast("你需要先登录")
        router.push({ path: '/login/' })
      }
    }
    return response;
  });
});

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount('#app')


