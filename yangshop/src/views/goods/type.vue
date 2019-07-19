<template>
  <div>
    <yang-header title="商品分类"/>
    <tab active-color="#f17c67">
      <tab-item
        @on-item-click="onClick(item.id)"
        :selected="item.id==category_id"
        v-for="(item, index) in $store.state.categories"
        :key="index"
      >{{ item.name }}</tab-item>
    </tab>

    <good-list :goods="goods"/>
    <van-button @click="getMore" :disabled="btnFlag" plain hairline type="danger" size="large">加载更多↓</van-button>
    <tabbar :tabactive="1"/>
  </div>
</template>

<script>
import goodList from "@/components/goods.vue";
import yangHeader from "@/components/header.vue";
import { Button } from "vant";
import { Tab, TabItem } from "vux";
import tabbar from "@/components/tabbar.vue";
import { isNull } from "util";
export default {
  components: {
    yangHeader,

    tabbar,
    goodList,
    Tab,
    TabItem,

    [Button.name]: Button
  },
  data() {
    return {
      goods: [],
      page: 1,
      category_id: this.$route.params.id,
      btnFlag: false
    };
  },
  methods: {
    onClick(id) {
      this.category_id = id;
      this.page = 1;
      this.goods = [];
      this.btnFlag = false;
      this.getGoods();
    },
    getGoods() {
      this.$http
        .get(`api/goods/?category=${this.category_id}&page=${this.page}`)
        .then(
          result => {
            if (result.status == 200) {
              this.goods = this.goods.concat(result.body.results);
              if (isNull(result.body.next)) {
                this.btnFlag = true;
              }
            }
          },
          () => {
            this.$toast("获取商品失败");
          }
        );
    },
    getMore() {
      this.page += 1;
      this.getGoods();
    }
  },
  created() {
    this.getGoods();
  }
};
</script>

