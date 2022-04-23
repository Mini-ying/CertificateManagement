<template>
  <div class="clearfix">
    <!-- 左上角校园logo -->
    <div class="logo">
      <img
        id="style2"
        src="../../assets/images/sztu.png"
        alt="logo"
        title="logo"
        width="15%"
      />
    </div>
    <div class="background">
      <!-- 登录部分 -->
      <div class="background_right">
        <p id="denglu1">欢迎使用数字证书管理系统</p>
        <hr />
        <!-- 准备好的容器 -->
        <div id="form_box">
          <!-- 登录数据的表单验证及名字 -->
          <el-form  :model="loginForm" ref="loginForm" >
            <!-- 用户输入ID -->
            <div class="layer1" >
              <img src="../../assets/images/id.png" />
              <!-- 用户输入的id存放在id -->
              <input
                type="text"
                v-model="loginForm.user_id"
                value
                placeholder="请输入ID"
                maxlength="15"
              />
            </div>
            <!-- 用户输入对应密码 -->
            <div class="layer1" >
              <img src="../../assets/images/mima.png" />
              <!-- 用户输入的密码存放在password -->
              <input
                type="password"
                v-model="loginForm.password"
                value
                placeholder="请输入密码"
                maxlength="30"
              />
            </div>
          </el-form>
          <div class="layer2">
            <!-- 点击登录触发事件login（）验证账号密码 -->
            <button class="login_nav" @click="login()">登录</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// import $ from "jquery";
// import { lunbo } from "../../JS/login";
// // import https from '@/api/https'
// import { postRequest } from '../../api/https'
export default {
  name: "login",
  data() {
    return {
      loginForm: {
        user_id: "001",
        password: "123456",
        // username: "",
        // phone: "",
      },
      // id1: ['admin', 'mini'],
      // password1: ['111', '222'], //存储用户名和密码的数据
      // username1: ['李赫海', '黄米妮'],
      // phone1:['13745678910','13910987654'],
      // index1: 0, //设置默认index值
      // rules:{
      //   user_id:[{required:true,message:'请输入用户名',trigger:'blur'}],
      //   password:[{required:true,message:'请输入密码',trigger:'blur'}]
      // },
      show: false //隐藏提示框
    };
  },
  methods: {
    login() {
      this.$refs.loginForm.validate((valid) => {
        if(valid){
          this.postRequest('http://127.0.0.1:5000/login',this.loginForm).then(resp=>{
            if(resp.re_code=="0"){
              //存贮用户token
              const tokenStr = resp.token;
              window.sessionStorage.setItem('tokenStr',tokenStr);
              //存用户id
              window.sessionStorage.setItem('user_id',this.loginForm.user_id);
              //存用户权限
              window.sessionStorage.setItem('role',resp.user.role);
              //路由跳转到主页面
              this.$router.replace({path:'/home'});
            }else{
              alert(resp.msg);
            }
          })
        }else{
          this.$message.error('登录失败');
          return false;
        }
      })
    },
  }
}
</script>

<style lang="less">
* {
  margin: 0;
  padding: 0;
}
.clearfix {
  content: "";
  display: block;
  clear: both;
  background:url("../../assets/images/welcome1.jpg") no-repeat;
  background-size:cover;
  background-attachment:fixed; 
}
img {
  max-width: 100%;
  max-height: 100%;
}
input {
  outline: none;
  border: none;
}
li {
  list-style-type: none;
}
.box_image {
  z-index: -1;
  position: absolute;
  width: 100%;
  height: 100%;
}
.logo {
  z-index: 1;
  position: relative;
  height: 10%;
  width: 100%;
}
.background {
  z-index: 1;
  width: 90%;
  height: 650px;
  margin: auto;
}
.background_right {
  margin: 10% 4.5%;
  height: 51%;
  width: 26%;
  float: right;
  background-color: white;
  border-radius: 30px;
}
img#style2 {
  margin: 1% 0 0 1%;
}
p#denglu1 {
  width: 72%;
  color: black;
  font-weight: bold;
  display: inline-block;
  margin: 20px 50px;
  text-align: center;
}
.layer1 {
  width: 76%;
  height: 40px;
  margin: 25px auto;
  border: 2px solid #ebe9e9;
}
.layer1 img {
  width: 30px;
  height: 30px;
  color: #555555;
  font-size: 16px;
  display: inline;
  border: 0px;
  margin: 5px 10px 5px 5px;
  vertical-align: middle;
}

.layer2 {
  margin: 6px auto;
}
.login_nav {
  height: 40px;
  width: 75%;
  margin: 1% 13% 3%;
  color: white;
  background-color: rgb(10, 100, 237);
  text-align: center;
  border: none;
  outline: none;
  border-radius: 10px;
}
.layer2 p{
  margin-left: 45%;
  font-size: 15px;
}
.layer2 a{
  color:red;
  text-align: center;
  border: none;
  // text-decoration: none;
  margin-left: 2%;
}
</style>
