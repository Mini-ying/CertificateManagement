<template>
<!--详情页 -->
  <div class="homepage">
    <div class="title">
      <!-- 首页 -->
    </div>
    <div>
      <p>欢迎使用数字证书系统</p>
      <img src="../../assets/images/welcome4.jpg" width="500px"/>
    </div>
  </div> 
</template>

<script>
export default {
  data (){
    return {
    }
  },
  computed: {
    obj () {
      return this.$store.state.obj
    },
  },
  methods: {
  }
}
</script>

<style lang="less">
.homepage {
  .title {
    font-size:18px;
    font-weight: 700;
  }

}
</style>