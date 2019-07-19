<template>
  <div>
    <x-header :title="title">
      <van-icon
        v-if="$store.state.userInfo.username"
        @click="show=true"
        slot="right"
        name="manager"
        size="20px"
      />
      <router-link v-else to="/login" slot="right">登录</router-link>
    </x-header>
    <van-actionsheet v-model="show" :actions="actions" cancel-text="取消" @select="onSelect"/>
  </div>
</template>

<script>
import { XHeader } from "vux";
import { Icon, Cell, Popup, Actionsheet, Dialog } from "vant";
export default {
  components: {
    XHeader,
    [Icon.name]: Icon,
    [Cell.name]: Cell,
    [Popup.name]: Popup,
    [Actionsheet.name]: Actionsheet,
    [Dialog.name]: Dialog
  },
  props: ["title"],
  data() {
    return {
      show: false,
      actions: [
        {
          name: "个人中心"
        },
        {
          name: "修改密码"
        },
        {
          name: "注销"
        }
      ]
    };
  },

  methods: {
    onSelect(item) {
      if (item.name == "修改密码") {
        Dialog.confirm({
          title: "修改密码",
          message: "确定修改密码？"
        })
          .then(() => {
            this.$router.push({ path: "/pwd" });
          })
          .catch(() => {
            this.show = false;
          });
      } else if (item.name == "注销") {
        Dialog.confirm({
          title: "注销",
          message: "确定注销当前账号？"
        })
          .then(() => {
            this.$router.push({ path: "/login" });
          })
          .catch(() => {
            this.show = false;
          });
      } else if (item.name == "个人中心") {
        this.$router.push({ path: "/user/account" });
      }
    }
  }
};
</script>

<style scoped>
div.vux-header {
  background: linear-gradient(90deg, rgb(166, 68, 255), rgb(255, 39, 25));
}
</style>
