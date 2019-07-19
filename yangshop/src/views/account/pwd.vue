<template>
  <div>
    <x-header title="找回密码">
      <router-link slot="right" to="/">
        <van-icon name="wap-home" size="20px"/>
      </router-link>
    </x-header>
    <group>
      <x-input
        title="手机"
        required
        v-model="userInfo.username"
        :show-clear="false"
        is-type="china-mobile"
        placeholder="请输入手机号"
      />
      <x-input title="图片验证码" v-model="captcha" :show-clear="false" placeholder="请输入图片验证码">
        <img @click="generateCaptcha" slot="right-full-height" :src="'http://api.shop.yanggebook.xyz/captcha/'+uuid" alt>
      </x-input>
      <x-input title="短信验证码" v-model="userInfo.code" :show-clear="false" placeholder="请输入短信验证码">
        <van-button @click="smsCode" slot="right-full-height" type="info" text="发送验证码"/>
      </x-input>
      <x-input
        title="新密码"
        required
        :min="6"
        :max="14"
        type="password"
        :show-clear="false"
        v-model="userInfo.password"
        placeholder="请输入新密码"
      />
      <x-input
        title="确认密码"
        required
        :min="6"
        :max="14"
        type="password"
        :show-clear="false"
        v-model="userInfo.re_password"
        placeholder="确认密码"
      />
      <van-button @click="change_pwd" size="large" type="primary" text="确认"/>
    </group>
  </div>
</template>

<script>
import guid from "@/assets/js/uuid.js";
import { XInput, Group, XHeader } from "vux";
import { Button, Icon } from "vant";
export default {
  data() {
    return {
      userInfo: {
        username: "",
        password: "",
        re_password: "",
        code: "",
      },
      captcha: "",
      uuid: guid()
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
    generateCaptcha() {
      this.uuid = guid();
    },
    smsCode() {
      let data = {
        username: this.userInfo.username,
        uuid: this.uuid,
        captcha: this.captcha,
        sms_category: "password"
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
    change_pwd(){
      let data = {
        username: this.userInfo.username,
        code: this.userInfo.code,
        password: this.userInfo.password,
        re_password: this.userInfo.re_password,
      };
      this.$http.put("api/user/1/", data).then(
        () => {
          this.$toast.success('修改密码成功')
          this.$router.push({ path: "/login" });
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
