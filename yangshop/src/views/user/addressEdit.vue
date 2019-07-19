<template>
  <div>
    <group>
      <x-input
        title="姓名"
        required
        v-model="addressInfo.name"
        :show-clear="false"
        is-type="china-name"
        placeholder="收货人姓名"
      />
      <x-input
        title="手机"
        required
        v-model="addressInfo.mobile"
        :show-clear="false"
        is-type="china-mobile"
        placeholder="收货人手机"
      />
      <x-input
        title="省份"
        required
        v-model="addressInfo.province"
        :show-clear="false"
        placeholder="输入省份"
      />
      <x-input title="市" required v-model="addressInfo.city" :show-clear="false" placeholder="输入市"/>
      <x-input
        title="县/区"
        required
        v-model="addressInfo.area"
        :show-clear="false"
        placeholder="输入县/区"
      />
      <x-input
        title="详细地址"
        required
        v-model="addressInfo.detail_address"
        :show-clear="false"
        placeholder="详细地址"
      />
      <van-button @click="updateAddress" size="large" type="danger" text="保存"/>
      <van-button @click="deleteAddress" size="large" plain text="删除"/>
    </group>
  </div>
</template>

<script>
import { XInput, Group } from "vux";
import { Button, Icon, Dialog } from "vant";
export default {
  data() {
    return {
      addressInfo: {
        name: "",
        mobile: "",
        province: "",
        city: "",
        area: "",
        detail_address: ""
      }
    };
  },
  components: {
    XInput,
    Group,

    [Button.name]: Button,
    [Icon.name]: Icon,
    [Dialog.name]: Dialog
  },
  methods: {
    getAddress() {
      this.$http.get(`api/user_address/${this.$route.params.id}`).then(
        res => {
          this.addressInfo = res.body;
        },
        () => {
          this.$Toast.fail("获取收获地址失败");
        }
      );
    },
    deleteAddress() {
      Dialog.confirm({
        title: "删除地址",
        message: "确定删除此地址吗？"
      })
        .then(() => {
          this.$http
            .delete(`api/user_address/${this.$route.params.id}`)
            .then(() => {
              this.$toast.success("删除成功！");
              this.$router.push({ path: "/user/address" });
            });
        })
        .catch(() => {});
    },
    updateAddress() {
      this.$http
        .put(`api/user_address/${this.$route.params.id}/`, this.addressInfo)
        .then(
          () => {
            this.$toast.success("修改成功！");
          },
          err => {
            let errArray = [];
            for (let i in err.body) {
              errArray = errArray.concat(err.body[i]);
            }
            this.$toast(errArray.join("，"));
          }
        );
    }
  },
  created() {
    this.$parent.active = 1;
    this.getAddress();
  }
};
</script>