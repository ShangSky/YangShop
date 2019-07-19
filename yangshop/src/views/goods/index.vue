<template>
  <div>
    <yang-header title="阳哥商城"/>

    <van-swipe :autoplay="3000">
      <van-swipe-item v-for="(item, goods) in banners" :key="goods">
        <router-link :to="'/detail/'+item.goods"><img style="width:100%;" :src="item.image"></router-link>
      </van-swipe-item>
    </van-swipe>
    <van-search placeholder="请输入搜索关键词" @focus="toSearch"/>
    <grid :cols="4" :show-lr-borders="false" :show-vertical-dividers="false">
      <grid-item v-for="(item, index) in $store.state.categories" :key="index" class="type-item" :label="item.name">
        <router-link slot="icon" :to="'/type/'+item.id"><img :src="item.image" class="type-img"></router-link>
      </grid-item>
    </grid>

    <good-list :goods="hot_goods"/>
    <tabbar :tabactive="0"/>
  </div>
</template>

<script>
import goodList from "@/components/goods.vue";
import tabbar from "@/components/tabbar.vue";
import yangHeader from "@/components/header.vue";
import { Grid, GridItem } from "vux";
import { Search, Swipe, SwipeItem } from "vant";
export default {
  components: {
    Grid,
    GridItem,
    [Search.name]: Search,
    [Swipe.name]: Swipe,
    [SwipeItem.name]: SwipeItem,

    yangHeader,
    goodList,
    tabbar
  },
  data() {
    return {
      banners: [],
      hot_goods: []
    };
  },
  methods: {
    toSearch() {
      this.$router.push({ path: "/search" });
    },
    getBanner() {
      this.$http.get("api/index_banner").then(result => {
        if (result.status == 200) {        
          this.banners = result.body;
        } else {
          this.$toast("获取轮播图失败");
        }
      })
    },
    getGoods() {
      this.$http.get("api/goods?ordering=-sold_num").then(result => {
        if (result.status == 200) {          
          this.hot_goods = result.body.results;
        } else {
          this.$toast("获取首页商品失败");
        }
      })
    }
    
  },
  created() {
    this.getBanner();
    this.getGoods();
  }
};
</script>

<style scoped>
div.van-swipe{
  touch-action: none;
}

.type-img {
  border-radius: 50%;
  height: 35px;
  width: 35px;
}

.type-item {
  padding: 10px 0;
}

.type-item:after {
  border: 0;
}

</style>

