<template>
  <div>
    <van-cell-group style="margin-bottom:5px;">
      <van-cell :title="name" size="large">
        <div slot="right-icon">
          <van-rate style="text-align: right;" :size="18" color="#FF3333" v-model="rate" readonly/>
          {{update_time |formatDate}}
        </div>

        <div slot="icon">
          <img
            class="avatar"
            :src="image"
            slot="label"
          >
        </div>
      </van-cell>
      <van-cell :value="content"/>
    </van-cell-group>
  </div>
</template>

<script>
import { Rate, CellGroup, Cell } from "vant";
export default {
  components: {
    [Cell.name]: Cell,
    [CellGroup.name]: CellGroup,
    [Rate.name]: Rate
  },
  props: ["name", "rate", "image", "update_time", "content"],
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
