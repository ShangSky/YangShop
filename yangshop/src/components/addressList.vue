<template>
  <div>
    <van-address-list
      :switchable="false"
      :list="setList()"
      @add="$router.push({ path: '/user/address/add' })"
      @edit="onEdit"
    />
  </div>
</template>

<script>
import { AddressList } from "vant";
export default {
  components: {
    [AddressList.name]: AddressList
  },
  props: ["addressList"],
  methods: {
    onEdit(item) {  
      this.$router.push({ path: `/user/address/edit/${item.id}` });
    },

    setList() {
      let list = [];
      for (var i of this.addressList) {
        list.push({
          id: i.id,
          name: i.name,
          tel: i.mobile,
          address: `${i.province}/${i.city}/${i.area} ${i.detail_address}`
        });
      }
      return list;
    }
  }
};
</script>

<style scoped>
button.van-address-list__add {
  bottom: 50px;
  z-index: 0;
}
</style>
