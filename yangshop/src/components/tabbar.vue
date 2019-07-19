<template>
  <van-tabbar v-model="active" active-color="red">
    <van-tabbar-item icon="wap-home" to="/">首页</van-tabbar-item>
    <van-tabbar-item icon="apps-o" :to="'/type/'+$store.state.categories[0]['id']">分类</van-tabbar-item>
    <van-tabbar-item icon="shopping-cart-o" v-if="cart_count==0" to="/cart">购物车</van-tabbar-item>
    <van-tabbar-item icon="shopping-cart-o" v-else :info="cart_count" to="/cart">购物车</van-tabbar-item>
    <van-tabbar-item icon="orders-o" to="/orders/info">订单</van-tabbar-item>
    <van-tabbar-item icon="manager-o" dot to="/user/account">我的</van-tabbar-item>
  </van-tabbar>
</template>

<script>
import { Tabbar, TabbarItem } from "vant";

export default {
  components: {
    [Tabbar.name]: Tabbar,
    [TabbarItem.name]: TabbarItem
  },
  props: ["tabactive"],
  data() {
    return {
      active: this.$props.tabactive,
      cart_count: 0
    };
  },
  methods: {
    getCartCount() {
      if (!this.$store.state.userInfo.username) {
        return;
      }

      this.$http.get("api/shopping_cart/").then(res => {
        this.cart_count = res.body.length;
      });
    }
  },
  created() {
    this.$store.commit("getCategory");
    this.getCartCount();
  }
};
</script>
