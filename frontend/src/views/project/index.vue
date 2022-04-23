<template>
  <!-- 项目管理详情页 -->
  <div class="project">
    <div class="title">
      项目管理
    </div>
    <el-card class="filter-container" shadow="never">
      <div>
        <i class="el-icon-search"></i>
        <span>筛选搜索</span>
        <!-- 查询搜索按钮，触发查询 -->
        <el-button style="float:right" type="primary"  @click="projectSearch()" size="small"  >
          查询搜索
        </el-button>
      </div>
      <div style="margin-top: 15px">
        <el-form  :inline="true" :model="project_SelectForm" ref="project_SelectForm" size="small"  label-width="140px"
        >
          <el-form-item label="输入搜索：">
            <select v-model="project_SelectForm.type" class="select1">
              <option disabled value="">请选择</option>
              <option value="project_id">项目ID</option>
              <option value="project_name">项目名称</option>
            </select>
            <el-input
              v-model="project_SelectForm.info"
              class="input-width"
            ></el-input>
          </el-form-item>
        </el-form>
      </div>
    </el-card>
    <el-card class="operate-container" shadow="never">
      <i class="el-icon-tickets"></i>
      <span>数据列表</span>
      <el-button type="primary" class="button1" @click="preview" size="small">添加项目</el-button>
      <!-- 添加项目的弹窗 -->
      <el-dialog title="添加项目" :visible.sync="dialogVisible" width="60%" :before-close="handleClose">
        <div id="pdfDom">
          <div class="proBox">
            <div class="chapter" v-show="isShow">
              <el-form :model="project_addForm" ref="project_addForm">
              <div class="layer03">
                <span style="margin-right: 25px">项目ID :</span>
                <input type="text" v-model=" project_addForm.project_id" maxlength="20"/>
              </div>
              <div class="layer03">
                <span style="margin-right: 25px">项目名称 :</span>
                <input type="text" v-model=" project_addForm.project_name" maxlength="20"/>
              </div>
              </el-form>
            </div>
          </div>
        </div>
        <span slot="footer" class="dialog-footer">
          <el-button @click="dialogVisible = false">取 消</el-button>
          <el-button @click="project_sumbit()">提交</el-button>
        </span>
      </el-dialog>
      <!-- 编辑项目的弹窗 -->
      <el-dialog title="编辑项目" :visible.sync="dialogVisible1" width="60%" :before-close="handleClose1">
        <div id="pdfDom">
          <div class="proBox">
            <div class="chapter" v-show="isShow">
              <el-form :model="project_editForm" ref="project_editForm">
              <div class="layer03">
                <span style="margin-right: 25px">项目ID :</span>{{project_editForm.project_id}}
              </div>
              <div class="layer03">
                <span style="margin-right: 25px">项目名称 :</span>
                <input type="text" v-model=" project_editForm.project_name" maxlength="20"/>
              </div>
              </el-form>
            </div>
          </div>
        </div>
        <span slot="footer" class="dialog-footer">
          <el-button @click="dialogVisible1 = false">取 消</el-button>
          <el-button @click="project_edit()">提交</el-button>
        </span>
      </el-dialog>
    </el-card>
    <!-- 列表 -->
   <el-table
    :data="Projectlist"
    style="width: 100%"
    max-height="320">
    <el-table-column
      fixed
      prop="project_id"
      label="项目编号"
      width="250">
    </el-table-column>
    <el-table-column
      prop="project_name"
      label="项目名"
      width="250">
    </el-table-column>
    <el-table-column
      fixed="right"
      label="操作"
      width="300">
      <template slot-scope="scope">
        <el-button  @click.native.prevent="check_info(scope.row.project_id, scope.row.project_name)"  type="text"  size="small">
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
      //项目数据列表
      Projectlist:[],

      //前端测试用户项目数据列表
      // Projectlist:  [{
      //     project_id: '111',
      //     project_name: '奥数竞赛',
      //   }, {
      //     project_id: '222',
      //     project_name: '外研杯竞赛',
      //   }, {
      //     project_id: '333',
      //     project_name: '大学生体育竞赛',
      //   }, {
      //     project_id: '888',
      //     project_name: '大数据杯',
      //   }, {
      //     project_id: '999',
      //     project_name: '校长杯',
      //   }],
      
      //查询的类别和关键字
      project_SelectForm: {
        type: "",
        info: "",
      },
      //要添加的项目id和项目名字
      project_addForm:{
        project_id: "",
        project_name: "",
      },
      //要编辑的项目id和项目名字
      project_editForm:{
        project_id: "",
        project_name: "",
      },
      project_delForm:{
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
    this.ProjectlistGet();
  },
  methods: {
    //获取项目数据
    ProjectlistGet(){
      this.getRequest('http://127.0.0.1:5000/projectList').then(resp=>{
        if(resp.re_code=="0"){
          this.Projectlist=resp.projects;
        }else{
              alert(resp.msg);
            }
      })
    },
    // 查询项目
    projectSearch() {
      this.$refs.project_SelectForm.validate((valid) => {
        if(valid){
          this.getRequest('http://127.0.0.1:5000/project',this.project_SelectForm).then(resp=>{
            // alert(JSON.stringify(resp));
            if(resp.re_code=="0"){
              //返回搜索结果
              //刷新数据列表
              this.Projectlist=resp.projects;
            }
            else{
                  this.$message.error('无该搜索结果');
                  return false;
                }
          })
        }
      })
    },
    // 添加弹窗关闭
    handleClose() {
      this.dialogVisible = false;
    },
    // 编辑弹窗关闭
    handleClose1() {
      this.dialogVisible1 = false;
    },
    // 添加弹窗显示
    preview() {
      this.dialogVisible = true;
    },
    // 添加新项目提交
    project_sumbit(){
      this.$refs.project_addForm.validate((valid) => {
        if(valid){
          this.postRequest('http://127.0.0.1:5000/project',this.project_addForm).then(resp=>{
            if(resp){
              alert("添加成功")
              //刷新数据列表
              this.ProjectlistGet();
              //弹窗的表单变为空值
              this.project_addForm.project_id="";
              this.project_addForm.project_name="";
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
    //查看该项目，跳转到届次页面
    check_info(val1, val2) {
      this.$router.push({
        path: "/sessions:project_id,project_name",
        query: { project_id: val1, project_name: val2 },
      });
    },
    //编辑项目按钮
    edit_info(index, data) {
      this.project_editForm=data;
      this.dialogVisible1 = true;
    },
     //编辑项目提交
    project_edit(){
      this.putRequest('http://127.0.0.1:5000/project',this.project_editForm).then(resp=>{
        if(resp.re_code=="0"){
          //刷新数据列表
          this.ProjectlistGet();
          //关闭弹窗
          this.handleClose1();
        }else{
              alert(resp.msg);
            }
      })
    },
    // 删除项目
    deleteRow(index, data) {
        // rows.splice(index, 1); //前端删除代码
        this.$confirm('此操作将永久删除['+data.project_name+']项目, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          //传给project_id统一名字（应该可以）
          this.project_delForm.project_id=data.project_id;
          this.deleteRequest('http://127.0.0.1:5000/project',this.project_delForm).then(resp=>{
            if(resp.re_code=="0"){
              this.$message({
              type: 'success',
              message: '删除成功!'
              });
              //刷新数据列表
              this.ProjectlistGet();
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
}
</style>
