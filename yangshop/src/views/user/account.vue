<template>
  <div>
    <group>
      <x-input style="padding:0 15px;" :show-clear="false" value="上传头像" :readonly="true">
        <img class="avatar" :src="userInfo.avatar" slot="label">
        <van-uploader :after-read="onRead" slot="right">
          <van-icon size="30px" name="upgrade"/>
        </van-uploader>
      </x-input>

      <x-input
        title="昵称"
        required
        v-model="userInfo.nickname"
        is-type="china-name"
        :show-clear="false"
        placeholder="请输入昵称"
        :readonly="readonly"
      />

      <x-input
        title="性别"
        :show-clear="false"
        :readonly="true"
        v-model="genderDisplay[userInfo.gender]"
      >
        <van-radio-group slot="right" v-model="userInfo.gender" :disabled="readonly">
          <flexbox :gutter="20">
            <flexbox-item>
              <van-radio name="male">男</van-radio>
            </flexbox-item>
            <flexbox-item>
              <van-radio name="female">女</van-radio>
            </flexbox-item>
          </flexbox>
        </van-radio-group>
      </x-input>

      <x-input
        title="邮箱"
        required
        v-model="userInfo.email"
        is-type="email"
        :show-clear="false"
        placeholder="请输入密码"
        :readonly="readonly"
      />

      <x-input title="手机" required v-model="userInfo.username" :show-clear="false" :readonly="true" />

      <x-textarea title="个人简介:" v-model="userInfo.desc" :readonly="readonly"/>

      <flexbox>
        <flexbox-item>
          <x-button type="warn" @click.native="readonly=false">修改</x-button>
        </flexbox-item>
        <flexbox-item>
          <x-button @click.native="saveUserInfo" :disabled="readonly" type="primary">保存</x-button>
        </flexbox-item>
      </flexbox>
    </group>
  </div>
</template>

<script>
import { XInput, Group, Flexbox, FlexboxItem, XButton, XTextarea } from "vux";
import { Button, Uploader, Icon, RadioGroup, Radio } from "vant";
import { isUndefined } from 'util';
export default {
  components: {
    XInput,
    Group,
    Flexbox,
    FlexboxItem,
    XButton,
    XTextarea,

    [Button.name]: Button,
    [Uploader.name]: Uploader,
    [Icon.name]: Icon,
    [RadioGroup.name]: RadioGroup,
    [Radio.name]: Radio
  },
  data() {
    return {
      userInfo: {},
      genderDisplay: { male: "男", female: "女" },
      readonly: true,
      avtar: ""
    };
  },
  methods: {
    onRead(file) {
      this.avatar = file;
      this.readonly = false;
    },
    saveUserInfo() {
      const formData = new FormData();
      formData.append("nickname", this.userInfo.nickname);
      formData.append("gender", this.userInfo.gender);
      formData.append("email", this.userInfo.email);
      formData.append("desc", this.userInfo.desc);
      if(!isUndefined(this.avatar)){
        formData.append("avatar", this.avatar.file);
      }
      this.$http
        .put("api/user_info/1/", formData, { "Content-Type": "Multipart/form-data" })
        .then(
          response => {
            this.userInfo = response.body;
            this.readonly = true;
          },
          () => {
            this.$Toast.fail("修改失败");
          }
        );
    },
    getUserInfo() {
      this.$http.get("api/user_info/1/").then(
        response => {
          this.userInfo = response.body;
        }
      );
    }
  },
  created() {
    this.$parent.active = 0;
    this.getUserInfo();
  }
};
</script>

<style scoped>
.avatar {
  height: 40px;
  width: 40px;
  border-radius: 50%;
  margin-right: 10px;
}
</style>
