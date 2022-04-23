<template>
<!-- 证书管理详情页 -->
  <div class="certificate" >
    <div class="title">
      证书管理
    </div>
    <el-card class="filter-container" shadow="never" >
      <div>
        <i class="el-icon-search"></i>
        <span>筛选搜索</span>
        <!-- 查询搜索按钮，触发查询 -->
        <el-button style="float:right" type="primary" @click="certificateSearch()" size="small"> 查询搜索 </el-button>
      </div>
      <div style="margin-top: 15px">
        <el-form :inline="true" :model="certificate_SelectForm" ref="certificate_SelectForm" size="small" label-width="140px">
          <el-form-item label="输入搜索：">
              <select v-model="certificate_SelectForm.type" class="select1">
                <option disabled value="">请选择</option>
                <option value="project_id">项目ID</option>
                <option value="session_id">届次ID</option>
                <option value="certificate_id">证书ID</option>
                <option value="certificate_name">证书名称</option>
                <option value="winner">获奖者名称</option>
                <!-- <option value="level">证书级别</option>
                <option value="datt">获奖日期</option>
                <option value="rank">获奖名次</option>
                <option value="giver">颁奖机构</option> -->
              </select>
            <el-input v-model="certificate_SelectForm.info" class="input-width" ></el-input>
          </el-form-item>
        </el-form>
      </div>
    </el-card>
    <el-card class="operate-container" shadow="never">
      <i class="el-icon-tickets"></i>
      <span>数据列表</span>
      <el-button type="primary" class="button1" @click="preview" size="small">添加证书</el-button>
      <el-dialog title="添加证书" :visible.sync="dialogVisible" width="60%" :before-close="handleClose">
            <div class="chapter" v-show="isShow" >
              <el-form :model="certificate_addForm" ref="certificate_addForm" >
              <div class="layer03">
                <span style="margin-right: 25px">项目ID :</span>
                <input type="text" v-model=" certificate_addForm.project_id" maxlength="20"/>
              </div>
              <div class="layer03">
                <span style="margin-right: 41px">届次ID :</span>
                <input type="text" v-model=" certificate_addForm.session_id" maxlength="20"/>
              </div>
              <div class="layer03">
                <span style="margin-right: 27px">证书ID :</span>
                <input type="text" v-model=" certificate_addForm.certificate_id" maxlength="20"/>
              </div>
              <div class="layer03">
                <span style="margin-right: 28px">证书名称 :</span>
                <input type="text" v-model=" certificate_addForm.certificate_name" maxlength="20"/>
              </div>
              <div class="layer03">
                <span style="margin-right: 15px">证书级别 :</span>
                <input type="text" v-model=" certificate_addForm.level" maxlength="20"/>
              </div>
              <div class="layer03">
                <span style="margin-right: 15px">获奖者名字 :</span>
                <input type="text" v-model=" certificate_addForm.winner" maxlength="20"/>
              </div>
              <div class="layer03">
                <span style="margin-right: 15px">证书名次 :</span>
                <input type="text" v-model=" certificate_addForm.rank" maxlength="20"/>
              </div>
              <div class="layer03">
                <span style="margin-right: 28px">获奖日期 :</span>
                <input type="text" v-model=" certificate_addForm.date" maxlength="20"/>
              </div>
              <div class="layer03">
                <span style="margin-right: 16px">颁奖机构 :</span>
                <input type="text" v-model=" certificate_addForm.giver" maxlength="20"/>
              </div>
              </el-form>
        </div>
        <span slot="footer" class="dialog-footer">
          <el-button @click="dialogVisible = false">取 消</el-button>
          <el-button @click="certificate_sumbit()">提交</el-button>
        </span>
      </el-dialog>
      <el-dialog title="编辑证书" :visible.sync="dialogVisible1" width="60%" :before-close="handleClose1">
            <div class="chapter" v-show="isShow">
              <el-form :model="certificate_editForm" ref="certificate_editForm">
              <div class="layer03" style="margin-right: 200px">
                <span style="margin-right: 29px">证书ID :</span>{{certificate_editForm.certificate_id}}
              </div>
              <div class="layer03">
                <span style="margin-right: 28px">证书名称 :</span>
                <input type="text" v-model=" certificate_editForm.certificate_name" maxlength="20"/>
              </div>
              <div class="layer03">
                <span style="margin-right: 15px">证书级别 :</span>
                <input type="text" v-model=" certificate_editForm.level" maxlength="20"/>
              </div>
              <div class="layer03">
                <span style="margin-right: 15px">获奖者名字 :</span>
                <input type="text" v-model=" certificate_editForm.winner" maxlength="20"/>
              </div>
              <div class="layer03">
                <span style="margin-right: 15px">证书名次 :</span>
                <input type="text" v-model=" certificate_editForm.rank" maxlength="20"/>
              </div>
              <div class="layer03">
                <span style="margin-right: 28px">获奖日期 :</span>
                <input type="text" v-model=" certificate_editForm.date" maxlength="20"/>
              </div>
              <div class="layer03">
                <span style="margin-right: 16px">颁奖机构 :</span>
                <input type="text" v-model=" certificate_editForm.giver" maxlength="20"/>
              </div>
              </el-form>
        </div>
        <span slot="footer" class="dialog-footer">
          <el-button @click="dialogVisible1 = false">取 消</el-button>
          <el-button @click="certificate_edit()">提交</el-button>
        </span>
      </el-dialog>
    </el-card>
    <el-dialog title="" :visible.sync="dialogVisible2" width="60%" :before-close="handleClose2" custom-class="cerifi">
      <el-button @click="download()">下载证书</el-button>
              <!-- <div id="pdfDom"> -->
                <div id="dom-to-img-wrapper" v-show="isShow" style="height:725px">
                  <!-- <canvas> -->
                    <img src="../../assets/images/certificate_background.png" style="position:absolute;width: 500px;height: 725px;margin-left: 140px;">
                  <div id="proBox" ref="imageDom">
                    <p class="tit">获奖证书</p>
                    <p class="proid"><span>编号：</span> 
                    <span>{{certificate_show.certificate_id}}</span></p>
                    <p class="con">
                    <span class="con-name">{{certificate_show.winner}}</span>
                    于
                    “{{certificate_show.certificate_name}}”
                    荣获{{certificate_show.level}}{{certificate_show.rank}}</p>
                    <p class="con">特发此证,予以鼓励</p>
                    <div class="con-unit">
                       <p>{{certificate_show.giver}}</p>
                      <p class="time">{{certificate_show.date}}</p>
                    </div>
                  </div>
                  <!-- </canvas> -->
               <!-- </div> -->
              </div>
              <span slot="footer" class="dialog-footer">
              </span>
            </el-dialog>
    <el-table
    :data="Certificatelist"
    style="width: 100%"
    max-height="320" >
    <el-table-column
      fixed
      prop="project_id"
      label="项目ID"
      width="120">
    </el-table-column>
    <el-table-column
      fixed
      prop="session_id"
      label="届次ID"
      width="120">
    </el-table-column>
    <el-table-column
      prop="certificate_id"
      label="证书编号"
      width="120">
    </el-table-column>
    <el-table-column
      prop="certificate_name"
      label="证书名称"
      width="200">
    </el-table-column>
    <el-table-column
      prop="winner"
      label="获奖人"
      width="120">
    </el-table-column>
    <el-table-column
      prop="level"
      label="获奖等级"
      width="100">
    </el-table-column>
    <el-table-column
      prop="date"
      label="获奖日期"
      width="120">
    </el-table-column>
    <el-table-column
      prop="rank"
      label="获奖名次"
      width="120">
    </el-table-column>
    <el-table-column
      prop="giver"
      label="颁奖机构"
      width="180">
    </el-table-column>
    <el-table-column
      fixed="right"
      label="操作"
      width="150">
      <template slot-scope="scope">
        <el-button  @click.native.prevent="show(scope.$index,scope.row)"  type="text"  size="small">
          查看证书
        </el-button>
        <el-button  @click.native.prevent="certificate_design(scope.$index, Certificatelist)"  type="text"  size="small">
          自定义证书
        </el-button>
        <el-button  @click.native.prevent="edit_info(scope.$index,scope.row)"  type="text"  size="small">
          编辑证书
        </el-button>
        <el-button  @click.native.prevent="deleteRow(scope.$index,scope.row)"  type="text"  size="small">
          删除
        </el-button>
      </template>
    </el-table-column>
    
  </el-table>
  </div>
</template>

<script>
import html2canvas from 'html2canvas'
export default {
  name:'certList',
  // inject:['reload'],
    data() {
      return {
        //证书数据列表数据
        Certificatelist:[],

        //前端测试数据
      //   Certificatelist: [
      //   {
      //     session:"第一届", //届次
      //     certificate_id:"123", //证书编号
      //     certificate_name:"校长杯篮球赛", //证书名称
      //     winner:"力大仙", //获奖者名称
      //     level:"校级", //证书级别
      //     date:"2020.1.1", //获奖日期
      //     rank:"第一名", //获奖名次
      //     giver:"深圳技术大学", //颁奖机构
      //   }, {
      //     session:"第一届", //届次
      //     certificate_id:"234", //证书编号
      //     certificate_name:"校长杯英语演讲大赛", //证书名称
      //     winner:"小文", //获奖者名称
      //     level:"校级", //证书级别
      //     date:"2020.1.1", //获奖日期
      //     rank:"第二名", //获奖名次
      //     giver:"深圳技术大学", //颁奖机构
      //   },{
      //     session:"第二届", //届次
      //     certificate_id:"8342690", //证书编号
      //     certificate_name:"口语大赛", //证书名称
      //     winner:"小明", //获奖者名称
      //     level:"校级", //证书级别
      //     date:"2020.6.23", //获奖日期
      //     rank:"第一名", //获奖名次
      //     giver:"深圳技术大学", //颁奖机构
      //   },{
      //     session:"第三十届", //届次
      //     certificate_id:"19857", //证书编号
      //     certificate_name:"奥数竞赛", //证书名称
      //     winner:"小黄", //获奖者名称
      //     level:"国家级", //证书级别
      //     date:"2021.5.21", //获奖日期
      //     rank:"一等奖", //获奖名次
      //     giver:"国家奥数竞赛委员会", //颁奖机构
      //   },{
      //     session:"第三十届", //届次
      //     certificate_id:"19856", //证书编号
      //     certificate_name:"奥数竞赛", //证书名称
      //     winner:"陈二二", //获奖者名称
      //     level:"国家级", //证书级别
      //     date:"2021.5.21", //获奖日期
      //     rank:"三等奖", //获奖名次
      //     giver:"国家奥数竞赛委员会", //颁奖机构
      //   },
      // ],

        //若从届次传过来，届次的数据
        Session:{
          session_id: "",
          project_id:""
        },
        certificate_SelectForm:{
          type: "",
          info: ""
        },
        certificate_show:{
          session:"", //届次
          certificate_id:"", //证书编号
          certificate_name:"", //证书名称
          winner:"", //获奖者名称
          level:"", //证书级别
          date:"", //获奖日期
          rank:"", //获奖名次
          giver:"", //颁奖机构
        },
        //证书添加
        certificate_addForm:{
          project_id:"",//项目号
          session_id:"", //届次
          certificate_id:"", //证书编号
          certificate_name:"", //证书名称
          winner:"", //获奖者名称
          level:"", //证书级别
          date:"", //获奖日期
          rank:"", //获奖名次
          giver:"", //颁奖机构
        },
        //证书编辑
        certificate_editForm:{
          project_id:"",//项目号
          session_id:"", //届次
          certificate_id:"", //证书编号
          certificate_name:"", //证书名称
          winner:"", //获奖者名称
          level:"", //证书级别
          date:"", //获奖日期
          rank:"", //获奖名次
          giver:"", //颁奖机构
        },
        certificate_delForm:{
          certificate_id:""
        },
       //添加框的标志值
      dialogVisible: false,
      //编辑框的标志值
      dialogVisible1: false,
      //证书的标志值
      dialogVisible2: false,
      isShow: true,
      }
    },
    async mounted() {
    // 获取datas
    this.Session.session_id=this.$route.query.session_id;
    window.sessionStorage.setItem('session_id', this.$route.query.session_id);
    // this.certificate_SelectForm.session_id=this.$route.query.session_id;
    // this.certificate_editForm.session_id=this.$route.query.session_id;
    // this.certificate_delForm.session_id=this.$route.query.session_id;

    this.Session.project_id=window.sessionStorage.getItem("project_id")
    this.CertificatelistGet();
  },
    methods:{
      //获取证书数据
    CertificatelistGet(){
      this.getRequest('http://127.0.0.1:5000/allCertificateList').then(resp=>{
        if(resp.re_code=="0"){
          this.Certificatelist=resp.certificates;
        }else{
              alert(resp.msg);
              return false;
            }
      })
    },
      // 通过关键词搜索
    certificateSearch(){
        this.$refs.certificate_SelectForm.validate((valid) => {
        if(valid){
          this.getRequest('http://127.0.0.1:5000/allCertificate',this.certificate_SelectForm).then(resp=>{
            if(resp.re_code=="0"){
              //返回搜索结果
              //刷新数据列表
              this.Certificatelist=resp.certificates;
            }
          })
        }else{
          this.$message.error('无该搜索结果');
          return false;
        }
      })
    },
    //添加 弹窗关闭
    handleClose() {
      this.dialogVisible = false;
    },
    // 编辑弹窗关闭
    handleClose1() {
      this.dialogVisible1 = false;
    },
    // 证书弹窗关闭
    handleClose2() {
      this.dialogVisible2 = false;
    },
    // 添加弹窗显示
    preview() {
      this.dialogVisible = true;
    },
    // 添加新证书提交
    certificate_sumbit(){
      this.$refs.certificate_addForm.validate((valid) => {
        if(valid){
          this.postRequest('http://127.0.0.1:5000/allCertificate',this.certificate_addForm).then(resp=>{
            if(resp.re_code=="0"){
              alert("添加成功")
              //刷新数据列表
              this.CertificatelistGet();
              //弹窗的表单变为空值
              this.certificate_addForm.project_id="";
              this.certificate_addForm.session_id="";
              this.certificate_addForm.certificate_id="";
              this.certificate_addForm.certificate_name="";
              this.certificate_addForm.winner="";
              this.certificate_addForm.level="";
              this.certificate_addForm.date="";
              this.certificate_addForm.rank="";
              this.certificate_addForm.giver="";
              //关闭弹窗
              this.handleClose();
            }else{
              alert(resp.msg);
              return false;
            }
          })
        }
      })
    },
    show(index, data){
      this.certificate_show=data;
      this.dialogVisible2 = true;
    },
    //编辑证书按钮
    edit_info(index, data) {
      this.certificate_editForm=data;
      this.dialogVisible1 = true;
    },
     //编辑证书提交
    certificate_edit(){
      alert(JSON.stringify(this.certificate_editForm));
      this.putRequest('http://127.0.0.1:5000/allCertificate',this.certificate_editForm).then(resp=>{
        if(resp.re_code=="0"){
          //刷新数据列表
          this.CertificatelistGet();
          //关闭弹窗
          this.handleClose1();
        }else{
              alert(resp.msg);
              return false;
            }
      })
    },
    // 删除证书
    deleteRow(index, data) {
        // rows.splice(index, 1); //前端删除代码
        this.$confirm('此操作将永久删除ID为['+data.certificate_id+']的证书, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.certificate_delForm.certificate_id=data.certificate_id;
          this.deleteRequest('http://127.0.0.1:5000/allCertificate',this.certificate_delForm).then(resp=>{
            if(resp.re_code=="0"){
              this.$message({
              type: 'success',
              message: '删除成功!'
              });
              //刷新数据列表
              this.CertificatelistGet();
            }else{
              this.$message.error('删除失败');
              return false;
            }
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          });          
        });
    },
    //下载证书
    download(){
      let domName = 'dom-to-img-wrapper'
      let imageDom = document.getElementById(domName)
      html2canvas(imageDom, {
        width: document.getElementById(domName).offsetWidth,  // canvas画板的宽度 一般都是要保存的那个dom的宽度
        height: document.getElementById(domName).offsetHeight,  // canvas画板的高度  同上
        scale: 1
      }).then((canvas) => {
        let base64Url = canvas.toDataURL('image/png', 1);
        this.fileDownload(base64Url)
      })
    },
    fileDownload(downloadUrl) {
      let a = document.createElement('a');
      a.style.display = 'none';
      a.href = downloadUrl;
      a.download = '证书.png';
      // 触发点击-然后移除
      document.body.appendChild(a);
      a.click();
      document.body.removeChild(a);
    }
  }
}
</script>

<style lang="less">
.certificate {
  .title {
    font-size:18px;
    font-weight: 700;
  }
  .el-input--small{
    float:left;
  }
  .is-never-shadow{
    margin-top: 10px;
  }
  .el-card__body{
    padding:10px 15px ;
  }
  .select1{
    height:25px;
  }
  .el-input__inner{
    height:30px;
    line-height:30px;
  }
  .button1{
    float:right;
    margin:0 15px 15px 0;
    background-color: #0668bc;
    color:white;
    border-radius: 5px;
    border-color:#0668bc;
  }
  .table_data{
    border: 1px solid #eff6fe;
  }
  table
        {
            border-collapse: collapse;
            margin: 0 auto;
            text-align: center;
        }
        table td, table th
        {
            border: 1px solid #cad9ea;
            color: #666;
            height: 30px;
        }
        table thead th
        {
            background-color: #eff6fe;
            width: 100px;
        }
        table tr:nth-child(odd)
        {
            background: #fff;
        }
        table tr:nth-child(even)
        {
            background: #eff6fe;
        }
        #proBox {
  // background: url("../../assets/images/certificate_background.png") no-repeat;
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
  .el-dialog__body{
    height:185px;
    padding:30px 0px 30px 120px;
  }   
  .el-dialog__footer{
    padding:0px 40px 20px;
  }
  .cerifi{
    height:900px;
    // padding:30px 0px 30px 120px;
  } 
}
</style>