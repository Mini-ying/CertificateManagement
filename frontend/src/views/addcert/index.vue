<template>
    <div class="addcert">
      
        <div class="title">
            添加证书
        </div>
        <form action="">
        <div class="layer04" id="certificate_input">
          <div class="layer03">
                <span style="margin-right: 25px">项目ID :</span>
                <input type="text" v-model=" Project.project_id" maxlength="15"/>
            </div>
            <div class="layer03">
                <span style="margin-right: 25px">项目名字 :</span>
                <input type="text" v-model=" Project.project_name" maxlength="15"/>
            </div>
            <div class="layer03">
                <span style="margin-right: 37px">届 次 :</span>
                <input type="text" v-model=" Certificate.sessions" maxlength="20"/>
            </div>
            <div class="layer03">
                <span style="margin-right: 25px">证书编号 :</span>
                <input type="text" v-model=" Certificate.certificate_id" maxlength="20"/>
            </div>
            <div class="layer03">
                <span style="margin-right: 10px">证书名称 :</span>
                <input type="text" v-model=" Certificate.certificate_name" maxlength="15"/>
            </div>
            <div class="layer03">
                <span style="margin-right: 11px">获奖者名称 :</span>
                <input type="text" v-model=" Certificate.winner" maxlength="15"/>
            </div>
            <div class="layer03">
                <span style="margin-right: 10px">证书级别 :</span>
                <input type="text" v-model=" Certificate.level" maxlength="15"/>
            </div>
            <div class="layer03">
                <span style="margin-right: 25px">获奖日期 :</span>
                <input type="text" v-model=" Certificate.date" maxlength="15"/>
            </div>
            <div class="layer03">
                <span style="margin-right: 10px">获奖名次 :</span>
                <input type="text" v-model=" Certificate.rank" maxlength="15"/>
            </div>
            <div class="layer03">
                <span style="margin-right: 25px">颁奖机构 :</span>
                <input type="text" v-model=" Certificate.giver" maxlength="15"/>
            </div> 
            <div class="layer06">
                <el-button @click="submit">提 交</el-button>
                <el-button @click="ResetData">重置</el-button>
            </div>
        </div>
        </form>
        <div class="mask" v-if="showModal" @click="showModal=false"></div>
        <div class="pop" v-if="showModal">
        <button @click="showModal=false" class="btn1">x</button>
        <div id="pdfDom">
        <div class="proBox" ref="imageDom">
          <p class="tit">获奖证书</p>
          <p class="proid"><span>编号：</span> <span>{{Certificate.certificate_id}}</span></p>
          <p class="con">
            <span class="con-name">{{Certificate.winner}}</span>
            于<span style="margin: 10px">{{Certificate.sessions}}</span>
            “{{Certificate.certificate_name}}”
            荣获{{Certificate.level}}{{Certificate.rank}}
          </p>
          <p class="con">特发此证,予以鼓励</p>
          <div class="con-unit">
            <p>{{Certificate.giver}}</p>
            <p class="time">{{Certificate.date}}</p>
          </div>
        </div>
      </div>
    </div>
    <button @click="showModal=true" class="btn">查看证书</button>
    </div>
</template>

<script>
export default {
  name:'certificate_input',
  data (){
    return {
      UserInfo: {
            id: "",
        },
        Project:{
          project_id:"",  //项目id
          project_name:"",   //项目名字
        },
    // 证书数据
      Certificate:{
        sessions:"",  //届次
        certificate_id:"",  //证书编号
        certificate_name:"",  //证书名称
        winner:"",  //获奖者名称
        level:"",  //证书级别
        date:"",  //获奖日期
        rank:"",  //获奖名次
        giver:"",  //颁奖机构
      },
      dialogVisible: false,
      pageData: null, //接收html格式代码
      htmlTitle: "荣誉证书",
      isShow: true,
      isCanvas: false,
      downType: true, // false为 pdf , true为图片
      showModal: false, //弹窗
    };
  },
  async mounted() {
    this.UserInfo.id = this.$route.query.id;
    this.Project.project_id=this.$route.query.project_id;
    this.Project.project_name=this.$route.query.project_name;
  },
  methods: {
    preview() {
      this.dialogVisible = true;
      this.$nextTick(() => {
        if (!this.isCanvas) {
          // 只绘画一次
          this.isCanvas = true;
          this.getChapter();
        }
    })
    },
    ResetData() {
        this.Certificate.sessions="";
        this.Certificate.certificate_id="";
        this.Certificate.certificate_name="";
        this.Certificate.winner="";
        this.Certificate.level="";
        this.Certificate.date="";
        this.Certificate.rank="";
        this.Certificate.giver="";
    },
    // 提交数据
    // submit(){
    //     // 传数据
    //     axios
    //     .post("http://127.0.0.1:8000/addcert", {
    //       sessions:this.Certificate.sessions,
    //       certificate_id:this.Certificate.certificate_id,
    //       certificate_name:this.Certificate.certificate_name,
    //       winner:this.Certificate.winner,
    //       level:this.Certificate.level,
    //       date:this.Certificate.date,
    //       rank:this.Certificate.rank,
    //       giver:this.Certificate.giver,
    //     })
    //     alert("提交成功");
    // },
  }
}

</script>

<style scoped>
.title {
    font-size:18px;
    font-weight: 700;
}
::v-deep .el-dialog__body {
  padding: 0px;
  display: flex;
  justify-content: center;
}
#pdfDom {
  /* 要想pdf周边留白，要在这里设置 */
  /* padding: 20px; */
  width: 750px;
  margin: 0 0 0 200px;
}
.el-dialog__header{
  padding: 25px 30px 0px;
}
.el-button--primary{
  background-color: rgb(6, 104, 188);
  border-color: rgb(6, 104, 188);
  padding: 10px 15px;
}
.proBox {
  background: url("../../assets/images/certificate_background.png") no-repeat;
  background-size: cover;
  width: 500px;
  height: 725px;
  padding: 145px 94px;
  box-sizing: border-box;
  margin: 0 auto;
  position: relative;
  color: #000;
  font-family: SimSun;
}
.tit {
  color: #7188ca;
  font-size: 36px;
  font-weight: 700;
  position: relative;
  top: -6px;
  left: 8px;
  letter-spacing: 20px;
  font-family: STHeiti;
  margin: 20px 0;
  text-align: center;
}
.proid {
  text-align: right;
  margin: 0;
  font-weight: 500;
  /* margin-right: 5px; */
}
.con {
  font-size: 20px;
  font-weight: 700;
  text-align: left;
  margin: 30px 0;
  line-height: 32px;
  text-indent: 2em;
}
.con-name {
  font-family: 华文行楷, STXingkai;
  border-bottom: 2px solid #000;
}
.con-unit {
  font-size: 18px;
  font-weight: 700;
  position: absolute;
  right: 60px;
  bottom: 130px;
  text-align: center;
  letter-spacing: 3px;
}
.con-unit p {
  margin: 5px 0;
}
.con-footer {
  font-size: 18px;
  font-weight: 700;
  position: absolute;
  bottom: 45px;
  left: 0;
  right: 0;
  text-align: center;
}
.chapter {
  border-radius: 50%;
  position: absolute;
  bottom: 75px;
  right: 134px;
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
}
.layer04{
  width:700px;
  height:180px;
  margin:50px 0 0 250px;
}
.layer06{
  margin-left:250px;
}
.mask {
  background-color: #000;
  opacity: 0.3;
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  z-index: 1
}
.pop {
  position: fixed;
  top: 0px;
  left: 200px;
  width: calc(100% - 600px);
  height:calc(100% - 200px);
  z-index: 2
}
.btn {
  background-color: #fff;
  border-radius: 4px;
  border: 1px solid blue;
  padding: 4px 12px;
}
.btn[data-v-4fc5b4de]{
  border: 1px solid #6c81b3;
  margin: 50px 0 0 530px;
  background: #6c81b3;
  color: white;
  text-align: center;
  box-sizing: border-box;
  font-weight: 500;
  padding: 12px 20px;
  font-size: 14px;
  border-radius: 4px;
}
.btn1[data-v-4fc5b4de]{
  float:right;
}
</style>