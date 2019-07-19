<template>
  <div>
    <van-swipe-cell v-for="(item, index) in userFav" :key="index" :right-width="60">
      <van-cell-group>
        <van-cell :to="'/detail'+item.goods.id" size="large">
          <img
            slot="title"
            style="height:40px; margin:0;"
            :src="item.goods.image"
            :alt="item.goods.name"
          >
          <van-tag type="primary">销量：{{ item.goods.sold_num }}</van-tag>
          <br>
          <van-tag type="danger">点击：{{ item.goods.click_num }}</van-tag>
          <br>
          <van-tag type="success">收藏：{{ item.goods.like_num }}</van-tag>
          <br>

          <div style="overflow:hidden;" slot="label">
            {{ item.goods.name }} &nbsp;
            <span style="color:red;">￥{{ item.goods.price }}</span>
          </div>
        </van-cell>
      </van-cell-group>
      <van-button
        @click="deleteFav(item.goods.id, index)"
        style="height:100%;"
        slot="right"
        type="danger"
      >删除</van-button>
    </van-swipe-cell>
  </div>
</template>

<script>
import { SwipeCell, Cell, CellGroup, Button, Tag } from "vant";
export default {
  components: {
    [SwipeCell.name]: SwipeCell,
    [Cell.name]: Cell,
    [CellGroup.name]: CellGroup,
    [Button.name]: Button,
    [Tag.name]: Tag
  },
  data() {
    return {
      userFav: []
    };
  },
  methods: {
    getUserFav() {
      this.$http.get("api/user_fav").then(
        response => {
          this.userFav = response.body;
        },
        err => {
          if (err.status == 401) {
            this.$toast("你未登录!");
          }
        }
      );
    },
    deleteFav(favId, index) {
      this.$http.delete(`api/user_fav/${favId}`).then(
       () => {
          this.userFav.splice(index, 1);
          this.$toast("删除成功!");
        },
        err => {
          if (err.status == 401) {
            this.$toast("你未登录!");
          }
        }
      );
    }
  },
  created() {
    this.$parent.active = 2;
    this.getUserFav();
  }
};
</script>

<style>
</style>
