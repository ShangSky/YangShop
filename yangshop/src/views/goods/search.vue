<template>
  <div>
    <yang-header title="查找商品"/>
    <van-search
      v-model="keyword"
      placeholder="请输入搜索关键词"
      show-action
      shape="round"
      @search="onSearch"
    >
      <div slot="action" @click="onSearch">搜索</div>
    </van-search>

    <tab>
      <tab-item
        v-for="(item, index) in sortList"
        :key="index"
        @on-item-click="goodsSort(item.sort)"
      >{{item.title}}</tab-item>
      <tab-item @on-item-click="show=true">筛选</tab-item>
    </tab>

    <goods-list :goods="goods"/>
    <van-button @click="getMore" :disabled="btnFlag" plain size="large" type="warning">加载更多↓</van-button>
    <tabbar :tabactive="-1"/>
    
    <van-popup v-model="show" position="top">
      <van-row>
        <van-radio-group v-model="category_id">
          <van-col span="12" v-for="(item, index) in $store.state.categories" :key="index">
            <van-radio :name="item.id">{{ item.name }}</van-radio>
          </van-col>
        </van-radio-group>
      </van-row>
      <van-row>
        <van-col span="8">
          <van-field v-model="minPrice" placeholder="最低价" />
        </van-col>
        <van-col span="8">
          <van-field v-model="maxPrice" placeholder="最高价" />
        </van-col>
        <van-col span="8">
          <van-button @click="onSearch" type="danger" style="width:100%;">确定</van-button>
        </van-col>
      </van-row>
    </van-popup>
  </div>
</template>

<script>
import { Search, Row, Col, Popup, RadioGroup, Radio, Field, Button } from "vant";
import { Tab, TabItem } from "vux";
import yangHeader from "@/components/header.vue";
import goodsList from "@/components/goods.vue";
import tabbar from "@/components/tabbar.vue";
import { isNull } from 'util';
export default {
  components: {
    [Search.name]: Search,
    [Popup.name]: Popup,
    [Row.name]: Row,
    [Col.name]: Col,
    [RadioGroup.name]: RadioGroup,
    [Radio.name]: Radio,
    [Field.name]: Field,
    [Button.name]: Button,

    Tab,
    TabItem,
    yangHeader,
    goodsList,
    tabbar,
  },
  methods: {
    onSearch() {
      this.page = 1;
      this.goods = []; 
      this.getGoods();
      this.show = false;
    },

    goodsSort(sort) {
      this.page = 1;
      this.goods = [];  
      this.sort = sort;
      this.getGoods();
    },

    getMore() {
      this.page += 1;
      this.getGoods();
    },

    getGoods() {
      this.$http.get(`api/goods/?category=${this.category_id}&page=${this.page}&ordering=${this.sort}&search=${this.keyword}&min_price${this.minPrice}=&max_price=${this.maxPrice}`).then(result => {
        if (result.status == 200) {
          this.goods = this.goods.concat(result.body.results);
          if (isNull(result.body.next)) {
            this.btnFlag = true;
          }else {
            this.btnFlag = false;
          }
        } else {
          this.$toast("获取商品失败");
        }
      });
    }
  },
  data() {
    return {
      show: false,
      btnFlag: true,
      goods: [],

      category_id: "",
      minPrice: '',
      maxPrice: '',
      keyword: "",
      page: 1,
      sort: '-create_time',
      sortList: [
        { title: "价格↓", sort: "price" },
        { title: "销量↑", sort: "-sold_num" },
        { title: "点击↑", sort: "-click_num" }
      ],
    };
  },
  created() {
    this.$store.commit("getCategory");
  },
};
</script>

<style scoped>
div.van-col--12 {
  margin-bottom: 10px;
  text-align: center;
}
div.van-col--8 {
  border: 1px solid #ccc;
}
</style>
