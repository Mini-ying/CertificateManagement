<template>
  <!-- 个人信息详情页 -->
  <div class="information">
    <div class="title">
      个人信息
    </div>
    <el-descriptions class="margin-top" title="" :column="3" :size="size" border>
    <template slot="extra">
      <el-button type="primary" class="button1" @click="preview" size="small">编辑</el-button>
    </template>
    <el-descriptions-item :span="3">
      <template slot="label">
        <i class="el-icon-postcard"></i>
        用户ID
      </template>
      {{this.UserInfo.user_id}}
    </el-descriptions-item>
    <el-descriptions-item :span="3">
      <template slot="label">
        <i class="el-icon-user"></i>
        用户名
      </template>
      {{this.UserInfo_show.username}}
    </el-descriptions-item>
    <el-descriptions-item :span="3">
      <template slot="label">
        <i class="el-icon-mobile-phone"></i>
        电话号码
      </template>
      {{this.UserInfo_show.phone}}
    </el-descriptions-item>
    <!-- <el-descriptions-item :span="3">
      <template slot="label">
        <i class="el-icon-coin"></i>
        密码
      </template>
      {{this.UserInfo_show.password}}
    </el-descriptions-item> -->
  </el-descriptions>
  <el-dialog title="编辑个人信息" :visible.sync="dialogVisible" width="60%" :before-close="handleClose">
        <div id="pdfDom">
          <div class="proBox">
            <div class="chapter" v-show="isShow">
              <el-form :model="UserInfo_edit" ref="UserInfo_edit">
              <div class="layer03">
                <span style="margin-right: 25px">用户ID :</span>{{UserInfo_edit.user_id}}
              </div>
              <div class="layer03">
                <span style="margin-right: 10px">用户名 :</span>
                <input type="text" v-model=" UserInfo_edit.username" maxlength="20"/>
              </div>
              <div class="layer03">
                <span style="margin-right: 15px">电话号码 :</span>
                <input type="text" v-model=" UserInfo_edit.phone" maxlength="20"/>
              </div>
              <div class="layer03">
                <span style="margin-right: 20px">密 码 :</span>
                <input type="password" v-model=" UserInfo_edit.password" maxlength="20"/>
              </div>
              <div class="layer03" style="margin-left:299px;">
                <span style="margin-right: 20px">再次输入密码 :</span>
                <input type="password" v-model=" UserInfo_edit.repassword" maxlength="20"/>
              </div>
              </el-form>
            </div>
          </div>
        </div>
        <span slot="footer" class="dialog-footer">
          <el-button @click="dialogVisible = false">取 消</el-button>
          <el-button @click="information_edit()">提交</el-button>
        </span>
      </el-dialog>
  </div>
</template>

<script>
export default {
  // inject: ["reload"],
  data() {
    return {
      //前端测试用数据
      
      UserInfo: {
        user_id: "",
      },
      UserInfo_show:{
        username: "",
        phone: "",
        // password: "",
        // password_again:"",
      },
      UserInfo_edit:{
        user_id:"",
        username: "",
        phone: "",
        password: "",
        repassword:""
        // password_again:"",
      },
      index1: 0, //设置默认index值
      // show: false //隐藏提示框
      //编辑框的标志值
      dialogVisible: false,
      isShow: true,
    };
    
  },
  computed: {
    obj() {
      return this.$store.state.obj;
    },
  },
  mounted (){
      this.UserInfo.user_id = window.sessionStorage.getItem('user_id');
      this.UserInfo_edit.user_id=window.sessionStorage.getItem('user_id');
      this.get_info();
  },
  // inject:["reload"],
  methods: {
    // 将用户信息存放在新类别UserInfo_edit，修改不成功不影响原用户信息
    get_info(){
      this.getRequest('http://127.0.0.1:5000/User').then(resp=>{
        if(resp.re_code=="0"){
          this.UserInfo_show=resp.user;
        }else{
          alert(resp.msg);
        }
      })
    },
    // 编辑弹窗关闭
    handleClose() {
      this.dialogVisible = false;
    },
    //编辑弹窗显示
    preview() {
      this.UserInfo_edit.username=this.UserInfo_show.username;
      this.UserInfo_edit.phone=this.UserInfo_show.phone;
      this.UserInfo_edit.password="";
      this.UserInfo_edit.repassword="";
      this.dialogVisible = true;
    },
     //编辑个人信息提交
    information_edit(){
      this.putRequest('http://127.0.0.1:5000/User',this.UserInfo_edit).then(resp=>{
        if(resp.re_code=="0"){
          //刷新数据列表
          this.UserInfo_show=resp.user; 
          alert(resp.msg);
          //关闭弹窗
          this.handleClose();
        }else{
          alert(resp.msg);
        }
      })
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
  .el-descriptions{
    width:700px;
    margin:40px auto;
  }
  .el-descriptions-item__cell.el-descriptions-item__label.is-bordered-label {
    width:200px;
  }
  .button1 {
    float: right;
    margin: 0 15px 15px 0;
    background-color: #0668bc;
    border:#0668bc;
    color: white;
    border-radius: 5px;
    width:68px;
    height:35px;
  }
  .layer03 {
  width:350px;
  height:40px;
  float:left;
  color:#2055b6;
}
.layer03 input{
  width:200px;
  height:23px;
  padding: 1px 2px;
  border-width: 2px;
  border-style: inset;
  border-color: -internal-light-dark(rgb(118, 118, 118));

}
.el-dialog__body {
  height:45px;
}
}
</style>
