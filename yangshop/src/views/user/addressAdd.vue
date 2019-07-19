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
      <van-button @click="saveAddress" size="large" type="danger" text="保存"/>
    </group>
  </div>
</template>

<script>
import { XInput, Group } from "vux";
import { Button, Icon } from "vant";
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
    [Icon.name]: Icon
  },
  methods: {
    saveAddress(){
      this.$http.post('api/user_address/', this.addressInfo).then(
        () => {
          this.$toast.success("保存成功")
          this.$router.push({path: '/user/address'})
        },
        err => {
          let errArray = [];
          for (let i in err.body) {
            errArray = errArray.concat(err.body[i]);
          }
          this.$toast(errArray.join('，'))
        }
      )
    }
  },
  created() {
    this.$parent.active = 1;
  }
};
</script>

