<template>
  <div>
    <x-header title="登录">
      <router-link slot="right" to="/">
        <van-icon name="wap-home" size="20px"/>
      </router-link>
    </x-header>
    <group>
      <x-input
        title="手机"
        required
        v-model="username"
        :show-clear="false"
        is-type="china-mobile"
        placeholder="请输入手机号"
      />
      <x-input
        title="密码"
        required
        :min="6"
        :max="14"
        type="password"
        :show-clear="false"
        v-model="password"
        placeholder="请输入密码"
      />
      <van-button @click="login" size="large" type="info" text="登录"/>
    </group>
    <div class="bottom-link">
      <router-link to="/pwd">忘记密码</router-link>
      <router-link to="/register">没有账号？去注册</router-link>
    </div>
  </div>
</template>

<script>
import { XInput, Group, XHeader } from "vux";
import { Button, Icon } from "vant";
import cookie from "@/assets/js/cookie.js";
export default {
  data() {
    return {
      username: "",
      password: ""
    };
  },
  components: {
    XHeader,
    XInput,
    Group,

    [Button.name]: Button,
    [Icon.name]: Icon
  },
  methods: {
    login() {
      let data = { username: this.username, password: this.password };
      this.$http.post("api/login/", data).then(
        result => {
          cookie.setCookie("username", this.username, 7);
          cookie.setCookie("token", result.body.token, 7);
          this.$store.commit("saveUserInfo");
          this.$toast('阳哥商城欢迎你！')
          this.$router.push({ path: "/index" });
        },
        () => {
          this.$toast("账号/密码错误");
        }
      );
    }
  },
  mounted() {
    cookie.delCookie("token");
    cookie.delCookie("username");
    this.$store.commit("saveUserInfo");
  }
};
</script>

<style scoped>
.bottom-link {
  display: flex;
  justify-content: space-between;
}

.bottom-link a {
  color: red;
}
</style>
<style scoped>
div.vux-header {
  background: linear-gradient(90deg, rgb(166, 68, 255), rgb(255, 39, 25));
}
</style>
