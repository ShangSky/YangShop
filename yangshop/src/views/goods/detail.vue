<template>
  <div>
    <yang-header title="商品详情"/>
    <van-swipe :autoplay="3000">
      <van-swipe-item>
        <img style="width:100%;" :src="goodsInfo.image">
      </van-swipe-item>
      <van-swipe-item v-for="(item, index) in goodsInfo.goods_banner" :key="index">
        <img style="width:100%;" :src="item.image">
      </van-swipe-item>
    </van-swipe>

    <van-panel
      :title="goodsInfo.name"
      :desc="goodsInfo.ship_free?'包邮':'不包邮'"
      :status="'￥'+goodsInfo.price"
    >
      <div style="padding:5px 15px;">{{ goodsInfo.desc }}</div>
    </van-panel>

    <van-cell-group>
      <van-cell>
        <van-row>
          <van-col span="8">点击：{{ goodsInfo.click_num }}</van-col>
          <van-col span="8">销量：{{ goodsInfo.sold_num }}</van-col>
          <van-col span="8">收藏：{{ goodsInfo.like_num }}</van-col>
        </van-row>
      </van-cell>
    </van-cell-group>

    <van-cell title="买家评论" icon="chat-o" :value="comments_count" is-link arrow-direction="down"/>

    <yang-comment
      v-for="(item, index) in comments"
      :key="index"
      :name="item.nickname"
      :rate="item.rate"
      :image="item.avatar"
      :update_time="item.update_time"
      :content="item.comment"
    />
    <van-button @click="getComments" :disabled="load_disabled" plain size="large" type="danger">加载更多</van-button>
    <van-goods-action style="z-index:1;">
      <van-goods-action-mini-btn
        icon="share"
        text="分享"
        class="copy"
        :data-clipboard-text="goodsUrl"
        @click="cpoyUrl"
      />
      <van-goods-action-mini-btn icon="like-o" text="收藏" @click="collectGoods"/>
      <van-goods-action-mini-btn icon="cart-o" text="购物车" @click="$router.push({ path: '/cart' })"/>
      <van-goods-action-big-btn text="加入购物车" @click="onAddCartClicked"/>
      <van-goods-action-big-btn primary text="立即购买" @click="buyClick"/>
    </van-goods-action>

    <van-popup v-model="show" position="bottom">
      <van-cell-group>
        <van-cell title="开心果" label="包邮">
          <span style="color:red;">{{ goodsInfo.price*buy_num|toFixed(2)}}</span>
        </van-cell>
        <van-cell title="购买数量" :label="'剩余'+goodsInfo.stock_num+'件'">
          <van-stepper v-model="buy_num"/>
        </van-cell>
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
        <van-button @click="onSubmit" type="danger" size="large">立即购买</van-button>
      </van-cell-group>
    </van-popup>
  </div>
</template>

<script>
import yangHeader from "@/components/header.vue";
import yangComment from "@/components/comment.vue";
import Clipboard from "clipboard";
import {
  GoodsAction,
  GoodsActionBigBtn,
  GoodsActionMiniBtn,
  Swipe,
  SwipeItem,
  Toast,
  Cell,
  CellGroup,
  Radio,
  RadioGroup,
  Field,
  Stepper,
  Button,
  Popup,
  Panel,
  Icon,
  Row,
  Col
} from "vant";
export default {
  components: {
    yangHeader,
    yangComment,
    [Swipe.name]: Swipe,
    [SwipeItem.name]: SwipeItem,
    [GoodsAction.name]: GoodsAction,
    [GoodsActionBigBtn.name]: GoodsActionBigBtn,
    [GoodsActionMiniBtn.name]: GoodsActionMiniBtn,
    [Cell.name]: Cell,
    [CellGroup.name]: CellGroup,
    [Field.name]: Field,
    [Stepper.name]: Stepper,
    [Button.name]: Button,
    [Popup.name]: Popup,
    [Panel.name]: Panel,
    [Icon.name]: Icon,
    [Row.name]: Row,
    [Col.name]: Col,
    [Radio.name]: Radio,
    [RadioGroup.name]: RadioGroup
  },
  filters: {
    toFixed: function(price, limit) {
      return price.toFixed(limit);
    }
  },
  data() {
    return {
      goodsUrl: window.location.href,
      show: false,
      comment_show: false,
      goodsInfo: {},
      addressList: [],
      comments: [],
      load_disabled: false,
      comments_count: 0,
      radio: 0,
      buy_num: 1,
      page: 1
    };
  },
  methods: {
    collectGoods() {
      this.$http.post(`api/user_fav/`, { goods: this.goodsInfo.id }).then(
        () => {
          this.goodsInfo.like_num++;
          this.$toast.success("收藏成功!");
        },
        err => {
          if (err.status == 400) {
            this.$toast.fail("已经收藏过该物品！");
          }
        }
      );
    },
    onAddCartClicked() {
      this.$http
        .post("api/shopping_cart/", {
          goods_num: 1,
          goods: this.$route.params.goodsId
        })
        .then(() => {
          Toast.success("加入成功");
        });
    },
    cpoyUrl() {
      let clipboard = new Clipboard(".copy");
      clipboard.on("success", function() {
        Toast.success("链接复制成功");
        clipboard.destroy();
      });
      clipboard.on("error", function() {
        clipboard.destroy();
      });
    },
    getDetail() {
      this.$http
        .get(`api/goods/${this.$route.params.goodsId}/`)
        .then(result => {
          this.goodsInfo = result.body;
        });
    },
    getComments() {
      this.$http
        .get(`api/goods_detail_comment/?goods=${this.$route.params.goodsId}&page=${this.page}`)
        .then(res => {
          this.comments = this.comments.concat(res.body.results);
          this.comments_count = res.body.count;
          this.page += 1
          
          if (!res.body.next) {
            this.load_disabled = true;
          }
        });
    },
    getAddress() {
      this.$http.get("api/user_address").then(res => {
        this.addressList = res.body;
      },
      () => {
        this.$toast("添加地址后才能购物")
      });
    },
    buyClick() {
      this.show = true;
      this.getAddress();
    },
    onSubmit() {
      let address = this.addressList[this.radio];
      let data = {
        order_goods: [{ goods: this.goodsInfo.id, goods_num: this.buy_num }],
        address: `${address.province}/${address.city}/${address.area} ${
          address.detail_address
        }`,
        receiver: address.name,
        mobile: address.mobile
      };
      this.$http.post("api/order/", data).then(res => {
        this.$toast.success("提交订单成功");
        location.href = res.body.pay_url;
      });
    }
  },
  mounted() {
    this.getDetail();
    this.getComments();
  }
};
</script>
<style scoped>
.avatar {
  height: 40px;
  width: 40px;
  border-radius: 50%;
  margin-right: 10px;
}
</style>