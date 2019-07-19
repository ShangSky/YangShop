<template id='app'>
  <div>
    <yang-header title="购物车"/>

    <van-swipe-cell v-for="(item, index) in cart_goods" :key="index" :right-width="60">
      <van-cell style="padding:0;">
        <van-card
          :num="item.goods_num"
          :tag="item.goods.name"
          :price="item.goods.price"
          :desc="item.goods.desc"
          :title="item.goods.name"
          :thumb="item.goods.image"
          :thumb-link="'/detail/'+item.goods.id"
        >
          <img slot="thumb" :src="item.goods.image" alt="商品图片">
          <div slot="footer" class="footer">
            <van-checkbox v-model="checked_list[index]" style="line-height:30px;"/>
            <van-stepper
              @change="onChange(item.goods_num, item.goods.stock_num, item.goods.id)"
              integer
              :max="item.goods.stock_num"
              v-model="item.goods_num"
            />
            <div
              style="color:red;font-size:16px;"
            >￥{{ item.goods_num*item.goods.price | toFixed(2) }}</div>
          </div>
        </van-card>
      </van-cell>
      <van-button
        @click="deleteShoppingCart(index, item.goods.id)"
        style="height:100%;"
        slot="right"
        type="danger"
      >删除</van-button>
    </van-swipe-cell>

    <van-radio-group v-model="radio">
      <van-cell-group>
        <van-cell
          v-for="(item, index) in addressList"
          :key="index"
          clickable
          @click="radio=index"
          size="large"
        >
          {{ item.mobile }}
          <van-radio :name="index"/>
          <div slot="title">{{ item.name }}</div>
          <div slot="label">
            {{ item.province }}/{{ item.city }}/{{ item.area }}
            <br>
            {{ item.detail_address }}
          </div>
        </van-cell>
      </van-cell-group>
    </van-radio-group>
    <van-button @click="$router.push({path: '/user/address/add'})" plain size="large" type="info">添加地址</van-button>
    <van-submit-bar
      style="position:static;"
      :price="getTotlalPrice()"
      :disabled="checked_list.indexOf(true) == -1"
      button-text="提交订单"
      @submit="onSubmit()"
    />

    <tabbar :tabactive="2"/>
  </div>
</template>

<script>
import {
  Cell,
  CellGroup,
  SwipeCell,
  Card,
  Button,
  Stepper,
  Checkbox,
  SubmitBar,
  Dialog,
  RadioGroup,
  Radio
} from "vant";
import yangHeader from "@/components/header.vue";
import tabbar from "@/components/tabbar.vue";
export default {
  components: {
    [Cell.name]: Cell,
    [CellGroup.name]: CellGroup,
    [SwipeCell.name]: SwipeCell,
    [Card.name]: Card,
    [Button.name]: Button,
    [Stepper.name]: Stepper,
    [Checkbox.name]: Checkbox,
    [SubmitBar.name]: SubmitBar,
    [Dialog.name]: Dialog,
    [RadioGroup.name]: RadioGroup,
    [Radio.name]: Radio,

    yangHeader,
    tabbar
  },
  filters: {
    toFixed: function(price, limit) {
      return price.toFixed(limit);
    }
  },
  data() {
    return {
      checked_list: [],
      cart_goods: [],
      addressList: [],
      radio: 0
    };
  },
  methods: {
    getTotlalPrice() {
      let totalPrice = 0.0;
      for (var i = 0; i < this.cart_goods.length; i++) {
        if (this.checked_list[i]) {
          totalPrice +=
            this.cart_goods[i].goods.price * this.cart_goods[i].goods_num;
        }
      }
      return totalPrice * 100;
    },
    getShoppingCart() {
      this.$http.get("api/shopping_cart/").then(res => {
        this.cart_goods = res.body;
        this.checked_list = new Array(this.cart_goods.length).fill(true);
      });
    },
    deleteShoppingCart(index, goods_id) {
      Dialog.confirm({
        title: "删除购物车纪录",
        message: "确定删除吗？"
      })
        .then(() => {
          this.$http.delete(`api/shopping_cart/${goods_id}/`).then(() => {
            this.$toast("删除成功");
            this.cart_goods.splice(index, 1);
            this.checked_list.splice(index, 1);
          });
        })
        .catch(() => {});
    },
    onChange(goods_num, stock_num, goods) {
      if (1 <= goods_num && goods_num <= stock_num) {
        let data = { goods, goods_num };
        this.$http.put(`api/shopping_cart/${goods}/`, data);
      }
    },
    getAddress() {
      this.$http.get("api/user_address").then(res => {
        this.addressList = res.body;
      },
      () => {
        this.$toast("添加地址后才能购物")
      });
    },
    onSubmit() {
      let order_goods = [];
      let address = this.addressList[this.radio];
      for (let i = 0; i < this.cart_goods.length; i++) {
        if (this.checked_list[i]) {
          order_goods.push({
            goods: this.cart_goods[i].goods.id,
            goods_num: this.cart_goods[i].goods_num
          });
          this.cart_goods.splice(i, 1);
        }
      }
      let data = {
        order_goods,
        address: `${address.province}/${address.city}/${address.area} ${
          address.detail_address
        }`,
        receiver: address.name,
        mobile: address.mobile
      };

      this.$http.post("api/order/", data).then(res => {
        this.$toast.success("提交订单成功");
        location.href = res.body.pay_url;
      },
      () => {
        this.$toast("提交订单失败")
      });
    }
  },
  created() {
    this.getShoppingCart();
    this.getAddress();
  }
};
</script>

<style scoped>
.footer {
  display: flex;
  justify-content: space-between;
}
</style>