<template>
  <div>
    <yang-header title="个人中心" />
    <button-tab :value='active'>
      <button-tab-item @on-item-click="jump('/user/account')">账号信息</button-tab-item>
      <button-tab-item @on-item-click="jump('/user/address')">收货信息</button-tab-item>
      <button-tab-item @on-item-click="jump('/user/fav')">我的收藏</button-tab-item>
    </button-tab>
    <router-view/>
    <tabbar :tabactive="4"/>
  </div>
</template>

<script>
import yangHeader from '@/components/header.vue';
import { ButtonTabItem, ButtonTab } from "vux";
import tabbar from "@/components/tabbar.vue";
export default {
  components: {
    ButtonTab,
    ButtonTabItem,
    tabbar,
    yangHeader
  },
  data() {
    return {
      active: 0
    };
  },
  methods: {
    jump(path) {
      this.$router.push({ path });
    }
  },
};
</script>

<style scoped>
  a.vux-button-group-current{
    background: linear-gradient(90deg, rgb(255, 39, 25), rgb(255, 97, 173))!important;
  }
  a.vux-button-tab-item:after, 
  a.vux-button-tab-item-first,
  a.vux-button-tab-item-last{
    border-radius: 0px!important;
    border: 0!important;
  }
  div.vux-button-group{
    border-bottom: 1px solid #ccc;
  }
  .weui-cells{
    margin-top: 0;
  }
</style>