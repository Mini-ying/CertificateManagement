<template>
<!-- 后台管理详情页 -->
  <div class="backstage">
    <div class="title">
      后台管理
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
                <option value="id">用户ID</option>
                <option value="uesername">用户名</option>
                <option value="phone">电话号码</option>
                <option value="password">密码</option>
              </select>
            <el-input v-model="select.selected_value" class="input-width" ></el-input>
          </el-form-item>
        </el-form>
      </div>
    </el-card>
    <el-card class="operate-container" shadow="never">
      <i class="el-icon-tickets"></i>
      <span>数据列表</span> 
      <el-button class="button1"  @click="preview" size="small"> 添加用户 </el-button>
      <!-- <el-dialog title="添加项目" :visible.sync="dialogble" width="60%" :before-close="handleClose">
        <div id="pdfDom">
          <div class="proBox">
            <div class="chapter" v-show="isShow">
              <div class="layer03">
                <span style="margin-right: 25px">项目ID :</span>
                <input type="text" v-model=" add_pro.project_id" maxlength="20"/>
              </div>
              <div class="layer03">
                <span style="margin-right: 25px">项目名称 :</span>
                <input type="text" v-model=" add_pro.project_name" maxlength="20"/>
              </div>
            </div>
          </div>
        </div>
        <span slot="footer" class="dialog-footer">
          <el-button @click="dialogble = false">取 消</el-button>
          <el-button @click="sumbit">提交</el-button>
        </span>
      </el-dialog> -->
    </el-card>
        <el-table :data="Certificate" border id="el-table" style="width: 100%">
        <!-- 动态循环的列表 -->
        <template  v-for="(item, index) in tableLabel">
          <el-table-column :key="index" :prop="item.prop" :label="item.label" width=""></el-table-column>
        </template>
        <!-- 固定的列：操作 -->
        <el-table-column label="操作">
          <template slot-scope="scope">
            <el-button size="small">编辑</el-button>
            <el-button @click="delete_pro(scope.row.project_id)" size="small" >删除</el-button>
            </template>
        </el-table-column>        
      </el-table>
  </div>
</template>

<script>

export default {
  name:'certList',
  inject:['reload'],
    data() {
      return {
        Certificate: [
        {
          id:"admin", //用户id
          username:"李赫海", //用户名
          phone:"13745678910", //电话号码
          password:"111", //密码
          jurisdiction:"1",//权限
        }, 
        {
          id:"mini", //用户id
          username:"黄米妮", //用户名
          phone:"13910987654", //电话号码
          password:"222", //密码
          jurisdiction:"2",//权限
        }, 
        {
          id:"lwt223", //用户id
          username:"Icy", //用户名
          phone:"143678265490", //电话号码
          password:"123", //密码
          jurisdiction:"2",//权限
        }, 
      ],
      tableLabel: [
          {label: '用户ID', prop: 'id'},
          {label: '用户名', prop: 'username'},
          {label: '电话号码', prop: 'phone'},
          {label: '密码', prop: 'password'},
          {label: '权限', prop: 'jurisdiction'},
      ],
        // 用户名
        UserInfo: {
            id: "",
        },
        select:{
          selected:"",
          selected_value:"",
        },
        user:{
          id:"", //
          username:"", //
          phone:"", //
          password:"", //
          jurisdiction:"",
        },
         //搜索选择的类别
        // listQuery:Object.assign({},defaultListQuery),
        // list:null,
        // total:null,
        // listLoading:false,
        // multipleSelection:[],
        // operateType:1,
        dialogble: false,
        pageData: null, //接收html格式代码
        // htmlTitle: "结业证书",
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
  },
    methods:{
      // 重置
      ResetSearch() {
        // this.listQuery = Object.assign({}, defaultListQuery);
      },
      // 弹窗关闭
      handleClose() {
        this.dialogble = false;
        // // 将数据清零
        // this.cert.sessions="";
        // this.cert.certificate_id="";
        // this.cert.certificate_name="";
        // this.cert.winner="";
        // this.cert.level="";
        // this.cert.date="";
        // this.cert.rank="";
        // this.cert.giver="";
      },
      // 弹窗显示
      preview() {
        this.dialogble = true;
        // // 将改行数据传到弹框
        // this.cert.sessions=sessions;
        // this.cert.certificate_id=certificate_id;
        // this.cert.certificate_name=certificate_name;
        // this.cert.winner=winner;
        // this.cert.level=level;
        // this.cert.date=date;
        // this.cert.rank=rank;
        // this.cert.giver=giver;
      },
      handleSearchList() {
        this.listQuery.pageNum = 1;
        this.getList();
      },
    }
}
</script>

<style lang="less">
.backstage {
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