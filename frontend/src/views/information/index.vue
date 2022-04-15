<template>
  <!-- 个人信息详情页 -->
  <div class="information">
    <div class="title">
      个人信息
    </div>
    <!-- 准备好的容器 -->
    <div class="box_info" id="form_box">
      <div class="shuru">
      <form action="">
        <!-- 展示用户ID -->
        <div class="layer01">
          <span style="margin-right: 44px">用 户 ID：</span>
          <!-- 用户输入的id存放在id -->
          {{UserInfo.id}}
        </div>
        <!-- 展示用户名 -->
        <div class="layer01">
          <span style="margin-right: 44px">用 户 名：</span>
          <!-- 用户输入的密码存放在suername -->
          <input type="text" v-model="UserInfo_change.username" maxlength="30" />
        </div>
        <div class="layer01">
          <span style="margin-right: 37px">电话号码：</span>
          <!-- 用户输入的密码存放在phone -->
          <input type="text" v-model="UserInfo_change.phone" maxlength="11" />
        </div>
        <div class="layer01">
           <span style="margin-right: 59px">密 码：  </span>
          <!-- 用户输入的密码存放在password -->
          <input type="text" v-model="UserInfo_change.password" maxlength="30" />
        </div>
        <div class="layer01">
          再次输入密码：
          <!-- 用户输入的密码存放在password -->
          <input type="text" v-model="UserInfo_change.password_again" maxlength="30" />
        </div>
      </form>
      <div class="layer2">
        <!-- 点击登录触发事件login（）验证账号密码 -->
        <button class="change_nav" @click="change">确认修改</button>
        <!-- <router-link to="./homepage">denglu </router-link> -->
      </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  // inject: ["reload"],
  data() {
    return {
      UserInfo:{
        id:"",
        password: "111",
        username: "李赫海",
        phone: "13745678910",
      },
      UserInfo_change:{
        password: "",
        username: "",
        phone: "",
        password_again:"",
      },
      index1: 0, //设置默认index值
      show: false //隐藏提示框
    };
    
  },
  computed: {
    obj() {
      return this.$store.state.obj;
    },
  },
  mounted (){
      this.UserInfo.id=this.$route.query.id;
      this.get();
      // this.reload();
  },
  inject:["reload"],
  methods: {
    // 将用户信息存放在新类别UserInfo_change，修改不成功不影响原用户信息
    get(){
      this.UserInfo_change.username=this.UserInfo.username;
      this.UserInfo_change.phone=this.UserInfo.phone;
      this.UserInfo_change.password=this.UserInfo.password;
      // this.reload();
    },
    // 判断用户名和电话号码是否有被修改，若被修改就修改该数据
    judge(){
      if(this.UserInfo_change.username!=this.UserInfo.username)
        {
          this.UserInfo.username=this.UserInfo_change.username;
        }
        if(this.UserInfo_change.phone!=this.UserInfo.phone)
        {
          this.UserInfo.phone=this.UserInfo_change.phone;
        }
        alert("个人信息已修改");
    },
    // 判断是否需要修改密码
    change() {
      // 若再次输入的密码为空值则默认不修改密码
      if(this.UserInfo_change.password_again=="")
      {
        // 如果密码被修改过则弹出消息提示需要再次输入密码
        if(this.UserInfo_change.password!=this.UserInfo.password)
        {
          alert("请再次输入密码");
        }
        // 如果密码没被修改过则只需要判断用户名和手机号码
        else{
          this.judge();
        }
      } 
      else{
        // 两次输入的密码一致才可以修改密码
        if(this.UserInfo_change.password_again==this.UserInfo_change.password)
        {
          this.judge();
          this.UserInfo.password=this.UserInfo_change.password;
          this.UserInfo_change.password_again="";
        }
        else{
          alert("两次输入的密码不一致，请重新修改");
        }
      }
    },
  },
};
</script>

<style lang="less">

.information {
  .title {
    font-size: 18px;
    font-weight: 700;
  }
  .box_info {
    width: 600px;
    height: 450px;
    margin: 35px 0 0 300px;
    border-radius: 30px;
    background: url(../../assets/images/blue1.png);
  }
  .shuru {
    padding-top: 30px;
  }
  .layer01 {
  width: 60%;
  height: 40px;
  margin: 18px auto;
  // border: 2px solid #ebe9e9;
  }
  .layer01 input{
    height:22px;
    border-radius: 5px;
    border: 1px solid #139be1;
  }
  .layer2 {
    margin: 25px auto;
  }
  .change_nav {
    height: 30px;
    width: 40%;
    margin: 18px 30%;
    color: rgb(55, 55, 206);
    font-size:14px;
    font-weight: bold;
    background-color: white;
    text-align: center;
    border: none;
    outline: none;
    border-radius: 5px;
  }
  
}
</style>
