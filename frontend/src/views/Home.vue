<template>
  <div class="home">
    <el-container>
      <el-header height="70px">
        <!-- <my-header></my-header> -->
        <!-- 页面头部信息 -->
        <div class="header">
          <div class="header-icon" >
            <span class="icon"></span>
            <div>数字证书管理系统</div>
          </div>
          <div class="header-tool" id="user">
            <el-dropdown>
              <span class="tool-one" @click="info">
                  Hello，{{this.UserInfo.user_id}}</span>
                  <!-- </router-link> -->
              <!-- 鼠标移到名字的位置可以选择退出系统 -->
              <el-dropdown-menu slot="dropdown">
                <el-dropdown-item @click.native="go">
                  退出系统
                </el-dropdown-item>
              </el-dropdown-menu>
            </el-dropdown>
          </div>
        </div>
      </el-header>
      <el-container>
        <el-aside v-if="getAsideType !== 0" :width="getAsideType === 1 ? '200px' : '200px'">
          <el-menu @select="menuClick" default-active="2" class="el-menu-vertical-demo" theme="dark" title="导航一">
              <el-menu-item index="/homepage">首页</el-menu-item>
              <el-menu-item index="/project">项目管理</el-menu-item>
              <el-menu-item index="/certificate">证书管理</el-menu-item>
              <el-menu-item index="/design">自定义证书</el-menu-item>
              <el-menu-item index="/backstage">后台管理</el-menu-item>
              <el-menu-item index="/information">个人信息</el-menu-item>
          </el-menu>
        </el-aside>
        <el-container>
          <!-- 页面中部，使用router方式 -->
          <el-main style="height: calc(100% - 78px);">
            <router-view />
          </el-main>
        </el-container>
      </el-container>
    </el-container>
  </div>
</template>

<script>
export default {
  name: "Home",
  components: {
  },
  data() {
    return {
      datas: [],
      UserInfo: {
        user_id: "",
      },
      index1: 0, //设置默认index值
      show: false, //隐藏提示框
      hide: true, //隐藏后台
    };
  },
  watch: {
    // 监听路由
    $route: {
      immediate: true, // 立即的，会先于create开启监听，在组件加载时就调用一次
      deep: true, // 开启深遍历，监听内部变化
      handler() {
        //  获取输入框内容，定位展开位置
        this.$store.commit("setInputValue", this.$route.query.inputValue);
      },
    },
  },
  computed: {
    getAsideType() {
      return this.$store.state.asideType;
    },
  },
  async mounted() {
    // 获取datas
    let datas = () => {
      return import("@/utils/datas.json");
    };
    this.datas = JSON.parse(JSON.stringify(await datas())).default;
    this.UserInfo.user_id = window.sessionStorage.getItem('user_id');
  },
  // inject:["reload"],
  methods: {
    //菜单栏选择路由跳转
    menuClick(index){
      //跳转后台需要判断权限
      if(index=="/backstage"){
        let role=window.sessionStorage.getItem('role');
        if(role=="administrator"){
          this.$router.push(index);
        }else{
          alert("您没有进入后台管理的权限！！！")
        }
      }else{
        this.$router.push(index);
      }
    },
    //隐藏后台管理
    // show_hide(){
    //   if(this.UserInfo.id =='admin'){
    //     this.hide=false;
    //   }
    // },
    //进入个人信息页面
    info(){
      this.$router.push('/information');
    },
    //退出系统
    go(){
      this.deleteRequest('http://127.0.0.1:5000/logout').then(resp=>{
        if(resp.re_code=="0"){
          alert("已退出系统");
          this.$router.replace({ path: '/'});
        }
      }) 
    },
  },
};
</script>

<style lang="less" scoped>
.home ::v-deep {
  height: 100%;
  .el-container {
    width: 100%;
    height: 100%;
  }
  .el-header {
    background: rgb(6, 104, 188);
    line-height: 48px;
    padding: 0;
  }
  .el-footer {
    border-top: 1px solid #ccc;
    line-height: 30px;
    font-size: 12px;
    color: #ccc;
    text-align: center;
  }
  .el-aside {
    border: 1px solid #ccc;
  }
  // 头部的css样式
  .header {
    clear: both;
    height: 100%;
    width: 100%;
    div {
      display: inline-block;
    }
    .header-icon {
      float: left;
      height: 70px;
      line-height: 70px;
      width: 200px;
      font-size: 18px;
      font-weight: 400;
      color: #fff;
      cursor: pointer;
      &:hover {
        font-weight: 700;
        color: #fff;
      }
      .icon {
        display: inline-block;
        width: 30px;
        height: 30px;
        margin: 20px 9px 9px 9px;
        background: url("~@/assets/icon.png") no-repeat center center;
        background-size: 26px 30px;
      }
      div {
        display: inline-block;
        vertical-align: top;
      }
    }
    .header-list {
      height: 100%;
      width: calc(100% - 420px);
      div {
        width: 100%;
        text-align: center;
        padding: 0 10px;
        color: white;
        font-size: 24px;
        font-weight: 700;
      }
    }
    .header-tool {
      float: right;
      height: 100%;
      width: 200px;
      text-align: end;
      padding-right: 20px;
      .tool-one {
        float: right;
        cursor: pointer;
        color: #fff;
        margin-top: 30px;
        margin-right: 30px;
      }
    }
  }
  // 菜单栏样式
  .meau{
    margin-top: 30px;
  }
  .meau li{
    height:40px;
    list-style: none;
    padding-left:20px;
  }
}
</style>
