<template>
  <panel style="margin-top:0;">
    <div slot="body">
      <div
        style="padding: 0 15px;"
        class="weui-media-box weui-media-box_text"
        v-for="(item, index) in goods"
        :key="index"
      >
        <router-link :to="'/detail/'+item.id">
          <div class="weui-media-box_appmsg">
          <div class="weui-media-box__hd">
            <img :src="item.image" class="weui-media-box__thumb">
          </div>
          <div class="weui-media-box__bd">
            <h4 class="weui-media-box__title">{{item.name}}</h4>
            <p class="weui-media-box__desc">{{item.desc}}</p>
          </div>
        </div>
        <ul class="weui-media-box__info">
          <li class="weui-media-box__info__meta">
            <span style="color:black;">
              <van-icon name="like-o"/>
              {{item.like_num}}
            </span>
          </li>
          <li class="weui-media-box__info__meta">
            <span style="color:orange;">{{item.sold_num}}人付款</span>
          </li>
          <li class="weui-media-box__info__meta weui-media-box__info__meta_extra">
            <span style="color:red;">￥{{item.price}}</span>
          </li>
        </ul>
        </router-link>
      </div>
    </div>
  </panel>
</template>

<script>
import { Panel } from "vux";
import { Icon } from "vant";
export default {
  props: ["goods"],
  components: {
    Panel,
    [Icon.name]: Icon
  }
};
</script>
