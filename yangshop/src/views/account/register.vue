<template>
  <div>
    <x-header title="注册">
      <router-link slot="right" to="/">
        <van-icon name="wap-home" size="20px"/>
      </router-link>
    </x-header>
    <group>
      <x-input
        title="手机"
        required
        v-model="registerInfo.username"
        :show-clear="false"
        is-type="china-mobile"
        placeholder="请输入手机号"
      />
      <x-input title="图片验证码" v-model="captcha" :show-clear="false" placeholder="请输入图片验证码">
        <img
          @click="generateCaptcha"
          slot="right-full-height"
          :src="'http://api.shop.yanggebook.xyz/captcha/'+uuid"
          height="100%"
        >
      </x-input>
      <x-input
        title="短信验证码"
        v-model="registerInfo.code"
        :show-clear="false"
        placeholder="请输入短信验证码"
      >
        <van-button @click="smsCode" slot="right-full-height" type="info" text="发送验证码"/>
      </x-input>
      <x-input
        title="密码"
        required
        :min="6"
        :max="14"
        type="password"
        :show-clear="false"
        v-model="registerInfo.password"
        placeholder="请输入密码"
      />
      <x-input
        title="确认密码"
        required
        :min="6"
        :max="14"
        type="password"
        :show-clear="false"
        v-model="registerInfo.re_password"
        placeholder="确认密码"
      />
      <van-button @click="register" size="large" type="primary" text="注册"/>
    </group>

    <router-link style="float:right; color: red;" to="/login">已有账号？去登录</router-link>
  </div>
</template>

<script>
import { XInput, Group, XHeader } from "vux";
import { Button, Icon } from "vant";
import guid from "@/assets/js/uuid.js";
import cookie from "@/assets/js/cookie.js";
export default {
  components: {
    XHeader,
    XInput,
    Group,
    [Button.name]: Button,
    [Icon.name]: Icon
  },
  data() {
    return {
      registerInfo: {
        username: "",
        password: "",
        re_password: "",
        code: ""
      },
      captcha: "",
      uuid: guid()
    };
  },
  methods: {
    generateCaptcha() {
      this.uuid = guid();
    },
    smsCode() {
      let data = {
        username: this.registerInfo.username,
        uuid: this.uuid,
        captcha: this.captcha,
        sms_category: "register"
      };
      this.$http.post("api/sms_code/", data).then(
        () => {
          this.$toast('验证码发送成功')
          
        },
        result => {
          let errArray = [];
          for (let i in result.body) {
            errArray = errArray.concat(result.body[i]);
          }     
          this.$toast(errArray.join('，'));
        }
      );
    },
    register(){
      let data = {
        username: this.registerInfo.username,
        code: this.registerInfo.code,
        password: this.registerInfo.password,
        re_password: this.registerInfo.re_password,
      };
      this.$http.post("api/user/", data).then(
        result => {
          cookie.setCookie("username", result.body.username, 7);
          cookie.setCookie("token", result.body.token, 7);
          this.$store.commit("saveUserInfo");
          this.$toast('阳哥商城欢迎你！')
          this.$router.push({ path: "/index" });
        },
        result => {
          let errArray = [];
          for (let i in result.body) {
            errArray = errArray.concat(result.body[i]);
          }     
          this.$toast(errArray.join('，'));
        }
      );
    }
  }
};
</script>
<style scoped>
div.vux-header {
  background: linear-gradient(90deg, rgb(166, 68, 255), rgb(255, 39, 25));
}
</style>
