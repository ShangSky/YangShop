<template>
  <div>
    <yang-address :addressList="addressList" />
  </div>
</template>

<script>
import yangAddress from "@/components/addressList";
export default {
  components: {
    yangAddress
  },
  data() {
    return {
      addressList: []
    };
  },

  methods: {
    getAddress() {
      this.$http.get("api/user_address").then(
        res => {
          this.addressList = res.body
        },
        () => {
          this.$Toast.fail('获取收获地址失败')
        }
      );
    },
  },

  created() {
    this.$parent.active = 1;
    this.getAddress();
  }
};
</script>
