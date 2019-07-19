<template>
  <div>
    <yang-header title="我的订单"/>
    <div class="router">
      <router-link tag="div" to="/orders/info">订单</router-link>
      <router-link tag="div" to="/orders/comments">评论</router-link>
    </div>
    <router-view />
    <tabbar :tabactive="3"/>
  </div>
</template>

<script>
import yangHeader from "@/components/header.vue";
import tabbar from "@/components/tabbar.vue";
export default {
  components: {
    yangHeader,
    tabbar
  }
};
</script>
<style scoped>
  .router{
    display:flex;justify-content:center;
    background: #fff;
  }
  .router div{
    flex:1;
    text-align: center;
    padding: 10px 5px;
    margin: 0 10px;
  }
  .router-link-exact-active{
    border-bottom: 3px solid red;
  }
</style>