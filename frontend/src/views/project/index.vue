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
            <select v-model="project_SelectForm.selected" class="select1">
              <option disabled value="">请选择</option>
              <option value="project_id">项目ID</option>
              <option value="project_name">项目名称</option>
            </select>
            <el-input
              v-model="project_SelectForm.selected_value"
              class="input-width"
            ></el-input>
          </el-form-item>
        </el-form>
      </div>
    </el-card>
    <el-card class="operate-container" shadow="never">
      <i class="el-icon-tickets"></i>
      <span>数据列表</span>
      <el-button type="primary" class="button1" @click="preview">添加项目</el-button>
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
    </el-card>
    <!-- 列表 -->
   <el-table
    :data="Project"
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
        <el-button  @click.native.prevent="deleteRow(scope.$index, Project)"  type="text"  size="small">
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
      Project:  [{
          project_id: '111',
          project_name: '奥数竞赛',
        }, {
          project_id: '222',
          project_name: '外研杯竞赛',
        }, {
          project_id: '333',
          project_name: '大学生体育竞赛',
        }, {
          project_id: '888',
          project_name: '大数据杯',
        }, {
          project_id: '999',
          project_name: '校长杯',
        }],
      // 用户id
      UserInfo: {
        id: "",
      },
      //搜索的类别和关键字
      project_SelectForm: {
        selected: "",
        selected_value: "",
      },
      //要添加的项目id和项目名字
      project_addForm:{
        project_id: "",
        project_name: "",
      },
      check_id: "",
      //搜索选择的类别
      dialogVisible: false,
      pageData: null, //接收html格式代码
      htmlTitle: "添加项目",
      isShow: true,
      isCanvas: false,
    };
  },
  async mounted() {
    // 获取datas
    // this.UserInfo.id = this.$route.query.id;
  },
  methods: {
    
    // 得到数列
    // getdata(){
    //   axios
    //     .get("http://127.0.0.1:8000/project")
    //     .then(function(project_id,project_name) {
    //       console.log(project_id,project_name);
    //       this.Project.project_id=project_id;
    //       this.Project.project_name=project_name;
    //     });
    // },
    
    // 通过关键词搜索待定
    projectSearch() {
      this.$refs.project_SelectForm.validate((valid) => {
        if(valid){
          this.postRequest('http://127.0.0.1:5000/project',this.project_SelectForm).then(resp=>{
            alert(JSON.stringify(resp));
            // alert(JSON.stringify(this.project_SelectForm));
            if(resp){
              //返回搜索结果
              alert("搜索成功")
            }
          })
        }else{
          this.$message.error('无该搜索结果');
          return false;
        }
      })
    },
    // 弹窗关闭
    handleClose() {
      this.dialogVisible = false;
    },
    // 弹窗显示
    preview() {
      this.dialogVisible = true;
    },
    // 添加新项目提交
    project_sumbit(){
      this.$refs.project_addForm.validate((valid) => {
        if(valid){
          this.postRequest('http://127.0.0.1:5000/project',this.project_addForm).then(resp=>{
            alert(JSON.stringify(resp));
            // alert(JSON.stringify(this.loginForm));
            if(resp){
              alert("添加成功")
            }
          })
        }else{
          this.$message.error('添加失败');
          return false;
        }
      })
    },
    // 删除项目
    deleteRow(index, rows) {
        rows.splice(index, 1);
    },
    //查看该项目
    check_info(val1, val2) {
      this.$router.push({
        path: "/pro_cert:id,project_id,project_name",
        query: { id: this.UserInfo.id, project_id: val1, project_name: val2 },
      });
      // ?uid(val);
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
}
}
</style>
