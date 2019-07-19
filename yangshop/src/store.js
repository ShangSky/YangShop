import Vue from 'vue'
import Vuex from 'vuex'
import cookie from "@/assets/js/cookie.js";
Vue.use(Vuex)

const userInfo = {
  username: cookie.getCookie('username'),
  token: cookie.getCookie('token')
};

export default new Vuex.Store({
  state: {
    categories: [{ 'id': 3 }],
    userInfo,
  },
  mutations: {
    getCategory(state) {
      if (state.categories.length == 1) {
        Vue.http.get("api/category").then(
          result => {
            if (result.status == 200) {
              state.categories = result.body;
            }
          }
        )
      }
    },

    saveUserInfo(state) {
      state.userInfo.username = cookie.getCookie('username')
      state.userInfo.token = cookie.getCookie('token')
    },
  },
  actions: {

  }
})
