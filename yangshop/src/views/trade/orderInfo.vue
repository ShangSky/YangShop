<template>
  <div>
    <van-cell-group style="margin-bottom:5px;" v-for="(item, index) in orders" :key="index">
      <van-cell title="订单号" :value="item.order_num"/>
      <van-cell title="总金额" :value="'¥'+item.total_price"/>
      <van-cell is-link v-if="item.pay_status=='交易创建'" title="支付状态">
        <a :href="item.pay_url">点击去支付</a>
      </van-cell>
      <van-cell v-else title="支付状态" :value="item.pay_status"/>
      <van-cell title="下单时间" :value="item.create_time | formatDate"/>
      <van-cell title="详细信息" @click="showDetail(index)">
        <van-icon slot="right-icon" name="label-o" class="custom-icon"/>
      </van-cell>
    </van-cell-group>

    <van-popup v-model="show" position="bottom">
      <van-cell title="关闭" @click="show=false">
        <van-icon slot="right-icon" name="cross" class="custom-icon"/>
      </van-cell>

      <van-cell title="订单号" :value="orderDetail.order_num"/>
      <van-cell title="交易号" :value="orderDetail.trade_num"/>
      <van-cell title="总金额" :value="'¥'+orderDetail.total_price"/>
      <van-cell title="运费" :value="'¥'+orderDetail.freight"/>
      <van-cell title="下单时间" :value="orderDetail.create_time | formatDate"/>
      <van-cell title="支付时间" :value="orderDetail.pay_time"/>
      <van-cell title="签收人" :value="orderDetail.receiver"/>
      <van-cell title="联系电话" :value="orderDetail.mobile"/>
      <van-cell>配送地址&nbsp;&nbsp;&nbsp;&nbsp;{{orderDetail.address}}</van-cell>
      <van-cell>
        <table style="width:100%;">
          <thead>
            <tr>
              <td>商品</td>
              <td>数量</td>
              <td>单价</td>
              <td>小计</td>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(order_goods, i) in orderDetail.order_goods" :key="i">
              <td>{{order_goods.goods.name}}</td>
              <td>{{order_goods.goods_num}}</td>
              <td>{{order_goods.goods.price}}</td>
              <td>{{(order_goods.goods_num * order_goods.goods.price) | toFixed(2)}}</td>
            </tr>
          </tbody>
        </table>
      </van-cell>
    </van-popup>
  </div>
</template>

<script>
import { Cell, CellGroup, Popup, Icon } from "vant";
export default {
  components: {
    [Cell.name]: Cell,
    [CellGroup.name]: CellGroup,
    [Popup.name]: Popup,
    [Icon.name]: Icon,
  },
  data() {
    return {
      activeNames: ["1"],
      show: false,
      orders: [],
      orderDetail: []
    };
  },
  methods: {
    getOrders() {
      this.$http.get("api/order/").then(res => {
        this.orders = res.body;
        this.show_list = new Array(this.orders.length).fill(false);
      });
    },
    showDetail(index) {
      this.show = true;
      this.orderDetail = this.orders[index];
    }
  },
  filters: {
    formatDate: function(val) {
      var value = new Date(val);
      var year = value.getFullYear();
      var month = value.getMonth() + 1;
      var day = value.getDate();
      var hour = value.getHours();
      var minutes = value.getMinutes();
      var seconds = value.getSeconds();
      return `${year}-${month}-${day} ${hour}:${minutes}:${seconds}`;
    },
    toFixed: function(price, limit) {
      return price.toFixed(limit);
    }
  },
  created() {
    this.getOrders();
  }
};
</script>