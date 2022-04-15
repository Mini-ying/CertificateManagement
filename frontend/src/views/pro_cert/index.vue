<template>
<!-- 项目-证书 -->
  <div class="pro_cert" >
    <div class="title">
      <span @click="reback">{{Project.project_name}}项目</span>
    </div>
    <el-card class="filter-container" shadow="never" >
      <div>
        <i class="el-icon-search"></i>
        <span>筛选搜索</span>
        <!-- 查询搜索按钮，触发查询 -->
        <el-button style="float:right" type="primary" @click="Search()" size="small"> 查询搜索 </el-button>
        <!-- 重置按钮，触发将数据重置 -->
        <el-button style="float:right;margin-right: 15px" @click="ResetSearch()" size="small"> 重置 </el-button>
      </div>
      <div style="margin-top: 15px">
        <el-form :inline="true" :model="listQuery" size="small" label-width="140px">
          <el-form-item label="输入搜索：">
              <select v-model="select.selected" class="select1">
                <option disabled value="">请选择</option>
                <option value="sessions">届次</option>
                <option value="certificate_id">证书编号</option>
                <option value="certificate_name">证书名称</option>
                <option value="winner">获奖者名称</option>
                <option value="level">证书级别</option>
                <option value="datt">获奖日期</option>
                <option value="rank">获奖名次</option>
                <option value="giver">颁奖机构</option>
              </select>
            <el-input v-model="select.selected_value" class="input-width" ></el-input>
          </el-form-item>
        </el-form>
      </div>
    </el-card>
    <el-card class="operate-container" shadow="never">
      <i class="el-icon-tickets"></i>
      <span>数据列表</span> 
      <el-button class="button1" @click="add_cert">添加证书</el-button>
    </el-card>
    <el-table :data="Pro_certificate" border id="el-table" style="width: 100%">
        <!-- 动态循环的列表 -->
        <template  v-for="(item, index) in tableLabel">
          <el-table-column :key="index" :prop="item.prop" :label="item.label" width=""></el-table-column>
        </template>
        <!-- 固定的列：操作 -->
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button @click="preview(scope.row.sessions,scope.row.certificate_id,scope.row.certificate_name,scope.row.winner,
            scope.row.level,scope.row.date,scope.row.rank,scope.row.giver)">查看证书</el-button>
            <el-dialog title="" :visible.sync="dialogVisible" width="60%" :before-close="handleClose">
              <div id="pdfDom">
                <div class="chapter" v-show="isShow">
                  <div class="proBox" ref="imageDom">
                    <p class="tit">获奖证书</p>
                    <p class="proid"><span>编号：</span> 
                    <span>{{cert.certificate_id}}</span></p>
                    <p class="con">
                    <span class="con-name">{{cert.winner}}</span>
                    于<span style="margin: 10px">{{cert.sessions}}</span>
                    “{{cert.certificate_name}}”
                    荣获{{cert.level}}{{cert.rank}}</p>
                    <p class="con">特发此证,予以鼓励</p>
                    <div class="con-unit">
                       <p>{{cert.giver}}</p>
                      <p class="time">{{cert.date}}</p>
                    </div>
                  </div>
               </div>
              </div>
              <span slot="footer" class="dialog-footer">
              <el-button @click="dialogVisible = false">关 闭</el-button>
              </span>
            </el-dialog>
            <el-button @click="delete_cert(scope.row.project_id)" >删除</el-button>
            </template>
        </el-table-column>        
      </el-table>
  </div>
</template>

<script>
// 重置
const defaultListQuery = {
    pageNum: 1,
    pageSize: 10,
    id: null,
    receiverKeyword: null,
    status: null,
    createTime: null,
    handleMan: null,
    handleTime: null
  };
export default {
  name:'pro_certList',
    data() {
      return {
        Pro_certificate: [
        {
          sessions:"第一届", //届次
          certificate_id:"123", //证书编号
          certificate_name:"abc", //证书名称
          winner:"力大仙", //获奖者名称
          level:"国家级", //证书级别
          date:"2020.1.1", //获奖日期
          rank:"第一名", //获奖名次
          giver:"深圳技术大学", //颁奖机构
        }, {
          sessions:"第一届", //届次
          certificate_id:"234", //证书编号
          certificate_name:"abc", //证书名称
          winner:"力大仙", //获奖者名称
          level:"国家级", //证书级别
          date:"2020.1.1", //获奖日期
          rank:"第一名", //获奖名次
          giver:"深圳技术大学", //颁奖机构
        }
      ],
      tableLabel: [
          {label: '届次', prop: 'sessions'},
          {label: '证书编号', prop: 'certificate_id'},
          {label: '证书名称', prop: 'certificate_name'},
          {label: '获奖者名称', prop: 'winner'},
          {label: '证书级别', prop: 'level'},
          {label: '获奖日期', prop: 'date'},
          {label: '获奖名次', prop: 'rank'},
          {label: '颁奖机构', prop: 'giver'},
      ],
        UserInfo: {
            id: "",
        },
        Project:{
          project_id:"",  //项目id
          project_name:"",   //项目名字
        },
        select:{
          selected:"",
          selected_value:"",
        },
        cert:{
          sessions:"", //届次
          certificate_id:"", //证书编号
          certificate_name:"", //证书名称
          winner:"", //获奖者名称
          level:"", //证书级别
          date:"", //获奖日期
          rank:"", //获奖名次
          giver:"", //颁奖机构
        },
      dialogVisible: false,
      pageData: null, //接收html格式代码
      htmlTitle: "结业证书",
      isShow: true,
      isCanvas: false,
      }
    },
    created(){
      this.getList();
    },
    async mounted() {
    this.UserInfo.id = this.$route.query.id;
    this.Project.project_id=this.$route.query.project_id;
    this.Project.project_name=this.$route.query.project_name;
  },
    methods:{
      // getdata(){
      // axios
      //   .get("http://127.0.0.1:8000/pro_cert")
      //   .then(function(sessions,certificate_id,certificate_name,winner,level,date,rank,giver) {
      //     this.Certificate.sessions=sessions;
      //     this.Certificate.certificate_id=certificate_id;
      //     this.Certificate.certificate_name=certificate_name;
      //     this.Certificate.winner=winner;
      //     this.Certificate.level=level;
      //     this.Certificate.date=date;
      //     this.Certificate.rank=rank;
      //     this.Certificate.giver=giver;
      //   });
      // },
      // 通过关键词搜索待定
      // Search(){
      //   // 向后台发送数据，得到结果
      //   axios
      //   .post("http://127.0.0.1:8000/project", {
      //     type: this.select.selected,
      //     info: this.select.selected_value,
      //   })
      //   .then(function(response) {
      //     console.log(response.status);
      //     if (parseInt(response.status) === 0) {
      //       //传入对应数据
      //     } else {
      //       alert("无该信息");
      //     }
      //   });
      // },
      // 重置
      ResetSearch() {
        this.listQuery = Object.assign({}, defaultListQuery);
      },
      // 弹窗关闭
      handleClose() {
        this.dialogVisible = false;
        // 将数据清零
        this.cert.sessions="";
        this.cert.certificate_id="";
        this.cert.certificate_name="";
        this.cert.winner="";
        this.cert.level="";
        this.cert.date="";
        this.cert.rank="";
        this.cert.giver="";
      },
      // 弹窗显示
      preview(sessions,certificate_id,certificate_name,winner,level,date,rank,giver) {
        this.dialogVisible = true;
        // 将改行数据传到弹框
        this.cert.sessions=sessions;
        this.cert.certificate_id=certificate_id;
        this.cert.certificate_name=certificate_name;
        this.cert.winner=winner;
        this.cert.level=level;
        this.cert.date=date;
        this.cert.rank=rank;
        this.cert.giver=giver;
      },
      // 删除证书
      // delete_cert(){
      //   axios
      //   .post("http://127.0.0.1:8000/pro_cert", {
      //     certificate_id: certificate_id,
      //   })
      //   alert("删除成功");
      // },
      // 返回项目
      reback(){
        this.$router.push({ path: '/project:id' ,query: {id:this.UserInfo.id}})
      },
      check_cert(val){
        this.cert.sessions=val;
      },
      // 添加证书跳转
      add_cert(){
        this.$router.push({ path: '/addcert:id,project_id,project_name' ,query: {id:this.UserInfo.id,project_id:this.Project.project_id,project_name:this.Project.project_name}});
      },
    }
}
</script>

<style lang="less">
.pro_cert {
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
  .button1 {
    float: right;
    margin: 0 15px 15px 0;
    background-color: #0668bc;
    border:#0668bc;
    color: white;
    border-radius: 5px;
  }
  .el-input__inner{
    height:30px;
    line-height:30px;
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
}
</style>