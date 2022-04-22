<template>
  <div id="app">
    <router-view></router-view>
    <!-- <router-view v-if="isRouterAlive"></router-view> -->
  </div>
</template>

<script>
  export default {
    name: "app",

  }
</script>

<style lang="less">
#app, html, body {
  margin: 0;
  padding: 0;
  width:100%;
  height:100%;
}
</style>
