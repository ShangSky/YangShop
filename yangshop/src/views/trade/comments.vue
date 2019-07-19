<template>
  <div>
    <van-cell
      v-for="(item, index) in noComments"
      :key="index"
      :title="item.goods.name"
      is-link
      @click="OnClick(item.id, index)"
      value="点击评论"
      size="large"
    />
    <yang-comment
      v-for="(item, index) in successComments"
      :key="index"
      :name="item.goods.name"
      :rate="item.rate"
      :image="item.goods.image"
      :update_time="item.update_time"
      :content="item.comment"
    />

    <van-popup style="width:100%;" v-model="show">
      <van-cell-group>
        <van-cell title="评分：">
          <van-rate v-model="commitCommentInfo.rate"/>
        </van-cell>
        <van-field
          v-model="commitCommentInfo.comment"
          label="评论内容："
          type="textarea"
          placeholder="请输入评论内容"
          rows="3"
          autosize
        />

        <van-button @click="commentSubmit" type="danger" size="large">发表评论</van-button>
        <van-button size="large" @click="show=false">取消</van-button>
      </van-cell-group>
    </van-popup>
  </div>
</template>

<script>
import yangComment from "@/components/comment.vue";
import { Cell, CellGroup, Field, Rate, Button, Popup } from "vant";
export default {
  components: {
    yangComment,
    [Cell.name]: Cell,
    [CellGroup.name]: CellGroup,
    [Field.name]: Field,
    [Rate.name]: Rate,
    [Button.name]: Button,
    [Popup.name]: Popup
  },
  data() {
    return {
      commitCommentInfo: {
        rate: 5,
        comment: ""
      },
      commentId: 0,
      show: false,
      commentIndex: 0,
      successComments: {},
      noComments: {}
    };
  },
  methods: {
    getNoComments() {
      this.$http.get("api/goods_comment?is_success=false").then(res => {
        this.noComments = res.body;
      });
    },

    getSuccessComments() {
      this.$http.get("api/goods_comment?is_success=true").then(res => {
        this.successComments = res.body;
      });
    },

    OnClick(id, index) {
      this.show = true;
      this.commentId = id;
      this.commentIndex = index;
    },
    commentSubmit() {
      this.$http
        .put(`api/goods_comment/${this.commentId}/`, this.commitCommentInfo)
        .then(res => {
          this.$toast.success("评论成功");
          this.noComments.splice(this.commentIndex, 1);
          this.successComments.unshift(res.body);
          this.show = false;
        });
    }
  },
  created() {
    this.getNoComments();
    this.getSuccessComments();
  }
};
</script>

