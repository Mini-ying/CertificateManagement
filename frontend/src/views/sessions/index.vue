<template>
  <!-- 项目管理详情页 -->
  <div class="project">
    <div class="title">
      届次管理><router-link to="/project">{{this.Project.project_id}}项目</router-link>>>届次
    </div>
    <el-card class="filter-container" shadow="never">
      <div>
        <i class="el-icon-search"></i>
        <span>筛选搜索</span>
        <!-- 查询搜索按钮，触发查询 -->
        <el-button style="float:right" type="primary"  @click="sessionSearch()" size="small"  >
          查询搜索
        </el-button>
      </div>
      <div style="margin-top: 15px">
        <el-form  :inline="true" :model="session_SelectForm" ref="session_SelectForm" size="small"  label-width="140px"
        >
          <el-form-item label="输入搜索：">
            <select v-model="session_SelectForm.type" class="select1">
              <option disabled value="">请选择</option>
              <option value="session_id">届次ID</option>
              <option value="number">届次</option>
              <option value="category">届次类别</option>
            </select>
            <el-input
              v-model="session_SelectForm.info"
              class="input-width"
            ></el-input>
          </el-form-item>
        </el-form>
      </div>
    </el-card>
    <el-card class="operate-container" shadow="never">
      <i class="el-icon-tickets"></i>
      <span>数据列表</span>
      <el-button type="primary" class="button1" @click="preview" size="small">添加届次</el-button>
      <!-- 添加届次的弹窗-->
      <el-dialog title="添加届次" :visible.sync="dialogVisible" width="60%" :before-close="handleClose">
        <div id="pdfDom">
          <div class="proBox">
            <div class="chapter" v-show="isShow">
              <el-form :model="session_addForm" ref="session_addForm">
              <div class="layer03">
                <span style="margin-right: 15px">项目ID :</span>
                <input type="text" v-model=" session_addForm.project_id" maxlength="20"/>
              </div>
              <div class="layer03">
                <span style="margin-right: 29px">届次ID :</span>
                <input type="text" v-model=" session_addForm.session_id" maxlength="20"/>
              </div>
              <div class="layer03">
                <span style="margin-right: 25px">届 次 :</span>
                <input type="text" v-model=" session_addForm.number" maxlength="20"/>
              </div>
              <div class="layer03">
                <span style="margin-right: 15px">届次类别 :</span>
                <input type="text" v-model=" session_addForm.category" maxlength="20"/>
              </div>
              </el-form>
            </div>
          </div>
        </div>
        <span slot="footer" class="dialog-footer">
          <el-button @click="handleClose()">取 消</el-button>
          <el-button @click="session_sumbit()">提交</el-button>
        </span>
      </el-dialog>
      <!-- 编辑届次的弹窗 -->
      <el-dialog title="编辑届次" :visible.sync="dialogVisible1" width="60%" :before-close="handleClose1">
        <div id="pdfDom">
          <div class="proBox">
            <div class="chapter" v-show="isShow">
              <el-form :model="session_editForm" ref="session_editForm">
              <div class="layer03" style="margin-right: 200px">
                <span style="margin-right: 29px">届次ID :</span>{{session_editForm.session_id}}
              </div>
              <div class="layer03">
                <span style="margin-right: 25px">届 次 :</span>
                <input type="text" v-model=" session_editForm.number" maxlength="20"/>
              </div>
              <div class="layer03">
                <span style="margin-right: 15px">届次类别 :</span>
                <input type="text" v-model=" session_editForm.category" maxlength="20"/>
              </div>
              </el-form>
            </div>
          </div>
        </div>
        <span slot="footer" class="dialog-footer">
          <el-button @click="dialogVisible1 = false">取 消</el-button>
          <el-button @click="session_edit()">提交</el-button>
        </span>
      </el-dialog>
    </el-card>
    <!-- 列表 -->
   <el-table
    :data="Sessionlist"
    style="width: 100%"
    max-height="320">
    <!-- <el-table-column
      fixed
      prop="project_id"
      label="项目ID"
      width="250">
    </el-table-column> -->
    <el-table-column
      fixed
      prop="session_id"
      label="届次ID"
      width="200">
    </el-table-column>
    <el-table-column
      prop="number"
      label="届次"
      width="250">
    </el-table-column>
    <el-table-column
      prop="category"
      label="届次类别"
      width="250">
    </el-table-column>
    <el-table-column
      fixed="right"
      label="操作"
      width="300">
      <template slot-scope="scope">
        <el-button  @click.native.prevent="check_info(scope.row.session_id,scope.row.number)"  type="text"  size="small">
          查看详情
        </el-button>
        <el-button  @click.native.prevent="edit_info(scope.$index,scope.row)"  type="text"  size="small">
          编辑
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
export default {
  name: "dataList",
  // inject:["reload"],
  data() {
    return {
      //数据列表数据
      Sessionlist:[],

      //前端测试用
      // Sessionlist:  [{
      //     session_id: '111',
      //     number: '第一届',
      //     category:'123',
      //   }, {
      //     session_id: '112',
      //     number: '第二届',
      //     category:'123',
      //   }, {
      //     session_id: '113',
      //     number: '第三届',
      //     category:'123',
      //   }, {
      //     session_id: '114',
      //     number: '第四届',
      //     category:'123',
      //   }, {
      //     session_id: '115',
      //     number: '第五届',
      //     category:'123',
      //   }],

      //项目信息
      Project:{
        project_id:"",
        project_name:"",
      },
      //搜索的类别和关键字
      session_SelectForm: {
        type: "",
        info: "",
        project_id:""
      },
      //要添加的项目id和项目名字
      session_addForm:{
        project_id: "",
        session_id: "",
        number:"",
        category:"",
      },
      //要编辑的项目id和项目名字
      session_editForm:{
        project_id:"",
        session_id: "",
        number:"",
        category:"",
      },
      session_delForm:{
        session_id:"",
        project_id:""
      },
      //添加框的标志值
      dialogVisible: false,
      //编辑框的标志值
      dialogVisible1: false,
      isShow: true,
    };
  },
  async mounted() {
    // 获取datas
    this.Project.project_id = window.sessionStorage.getItem('project_id');
    this.Project.project_name = window.sessionStorage.getItem('project_name');
    this.SessionlistGet();
  },
  methods: {
     //获取届次数据
    SessionlistGet(){
      this.getRequest('http://127.0.0.1:5000/sessionList',this.Project).then(resp=>{
        if(resp.re_code=="0"){
          // this.Sessionlist.project_id=window.sessionStorage.getItem("project_id");
          this.Sessionlist=resp.sessions;
        }else{
              alert(resp.msg);
            }
      })
    },
    // 通过关键词搜索待定
    sessionSearch() {
      this.$refs.session_SelectForm.validate((valid) => {
        if(valid){
          this.session_SelectForm.project_id=window.sessionStorage.getItem("project_id");
          this.getRequest('http://127.0.0.1:5000/session',this.session_SelectForm).then(resp=>{
            // alert(JSON.stringify(resp));
            if(resp.re_code=="0"){
              //返回搜索结果
              //刷新数据列表
              this.Sessionlist=resp.sessions;
            }else{
              this.Sessionlist="";
              this.$message.error('无该搜索结果');
              return false;
            }
          })
        }else{
          this.$message.error('无该搜索结果');
          return false;
        }
      })
    },
    //添加内容重置
    Reset(){
      this.session_addForm.project_id="";
      this.session_addForm.session_id="";
      this.session_addForm.number="";
      this.session_addForm.category="";
    },
    // 添加弹窗关闭
    handleClose() {
      this.dialogVisible = false;
      this.Reset();
    },
    // 编辑弹窗关闭
    handleClose1() {
      this.dialogVisible1 = false;
    },
    // 添加弹窗显示
    preview() {
      this.dialogVisible = true;
    },
    // 添加新届次提交
    session_sumbit(){
      this.$refs.session_addForm.validate((valid) => {
        if(valid){
          this.postRequest('http://127.0.0.1:5000/session',this.session_addForm).then(resp=>{
            if(resp.re_code=="0"){
              alert("添加成功")
              //刷新数据列表
              this.SessionlistGet();
              //弹窗的表单变为空值
              this.Reset();
              //关闭弹窗
              this.handleClose();
            }else{
              alert(resp.msg);
              return false;
            }
          })
        }else{
          this.$message.error('添加失败');
          return false;
        }
      })
    },
    //查看该届次的证书
    check_info(val1,val2) {
      window.sessionStorage.setItem('session_id', val1);
      window.sessionStorage.setItem('number', val2);
      this.$router.push({
        path: "/session-certificate"});
    },
    //编辑届次按钮
    edit_info(index, data) {
      this.session_editForm=data;
      this.dialogVisible1 = true;
    },
     //编辑届次提交
    session_edit(){
      this.session_editForm.project_id=window.sessionStorage.getItem("project_id");
      this.putRequest('http://127.0.0.1:5000/session',this.session_editForm).then(resp=>{
        if(resp.re_code=="0"){
          //刷新数据列表
          this.SessionlistGet();
          alert(resp.msg);
          //关闭弹窗
          this.handleClose1();
          
        }else{
              alert(resp.msg);
              return false;
            }
      })
    },
    //删除届次
    deleteRow(index, data) {
        // rows.splice(index, 1); //前端删除代码
        this.$confirm('此操作将永久删除['+data.number+']届次, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.session_delForm.session_id=data.session_id;
          this.session_delForm.project_id=window.sessionStorage.getItem("project_id");
          this.deleteRequest('http://127.0.0.1:5000/session',this.session_delForm).then(resp=>{
            if(resp.re_code=="0"){
              this.$message({
              type: 'success',
              message: '删除成功!'
              });
              //刷新数据列表
              this.SessionlistGet();
            }else{
              alert(resp.msg);
            }
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          });          
        });
    },
  },
};
</script>

<style lang="less">
.project {
  .title {
    font-size: 18px;
    font-weight: 700;
  }
  .el-input--small {
    float: left;
  }
  .is-never-shadow {
    margin-top: 10px;
  }
  .el-card__body {
    padding: 10px 15px;
  }
  .el-dialog__footer{
    padding:0px 40px 20px;
  }
  .el-dialog__body{
    padding:30px 0px 30px 120px;

  }
  .select1 {
    height: 25px;
  }
  .button1 {
    float: right;
    margin: 0 15px 15px 0;
    background-color: #0668bc;
    border:#0668bc;
    color: white;
    border-radius: 5px;
  }
  .el-input__inner {
    height: 30px;
    line-height: 30px;
  }
  .table_data {
    border: 1px solid #eff6fe;
  }
  table {
    border-collapse: collapse;
    margin: 0 auto;
    text-align: center;
  }
  table td,
  table th {
    border: 1px solid #cad9ea;
    color: #666;
    height: 30px;
  }
  table thead th {
    background-color: #eff6fe;
    width: 100px;
  }
  table tr:nth-child(odd) {
    background: #fff;
    height: 50px;
  }
  table tr:nth-child(even) {
    background: #eff6fe;
    height: 50px;
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
    height:70px;
  }
  .router-link-active {
  text-decoration: none;
  color: #2055b6;
 }
 a {
  text-decoration: none;
  color: #2055b6;
 }
}
</style>
