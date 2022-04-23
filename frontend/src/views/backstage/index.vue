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
        <el-button style="float:right" type="primary" @click="backstageSearch()" size="small"> 查询搜索 </el-button>
      </div>
      <div style="margin-top: 15px">
        <el-form :inline="true" :model="listQuery" size="small" label-width="140px">
          <el-form-item label="输入搜索：">
              <select v-model="backstage_SelectForm.type" class="select1">
                <option disabled value="">请选择</option>
                <option value="user_id">用户ID</option>
                <option value="username">用户名</option>
                <option value="phone">电话号码</option>
                <!-- <option value="password">密码</option> -->
                <option value="role">权限</option>
              </select>
            <el-input v-model="backstage_SelectForm.info" class="input-width" ></el-input>
          </el-form-item>
        </el-form>
      </div>
    </el-card>
    <el-card class="operate-container" shadow="never">
      <i class="el-icon-tickets"></i>
      <span>数据列表</span> 
      <el-button class="button1"  @click="preview" size="small"> 添加用户 </el-button>
      <!-- 添加用户弹窗 -->
      <el-dialog title="添加用户" :visible.sync="dialogVisible" width="60%" :before-close="handleClose">
        <div id="pdfDom">
          <div class="proBox">
            <div class="chapter" v-show="isShow">
              <el-form :model="backstage_addForm" ref="backstage_addForm">
              <div class="layer03">
                <span style="margin-right: 28px">用户ID :</span>
                <input type="text" v-model=" backstage_addForm.user_id" maxlength="20"/>
              </div>
              <div class="layer03">
                <span style="margin-right: 10px">用户名字 :</span>
                <input type="text" v-model=" backstage_addForm.username" maxlength="20"/>
              </div>
              <div class="layer03">
                <span style="margin-right: 15px">电话号码 :</span>
                <input type="text" v-model=" backstage_addForm.phone" maxlength="20"/>
              </div>
              <!-- <div class="layer03">
                <span style="margin-right: 38px">密码 :</span>
                <input type="text" v-model=" backstage_addForm.password" maxlength="20"/>
              </div> -->
              <div class="layer03">
                <span style="margin-right: 15px">用户权限 :</span>
                <input type="text" v-model=" backstage_addForm.role" maxlength="20"/>
              </div>
              </el-form>
            </div>
          </div>
        </div>
        <span slot="footer" class="dialog-footer">
          <el-button @click="dialogVisible = false">取 消</el-button>
          <el-button @click="backstage_sumbit()">提交</el-button>
        </span>
      </el-dialog>
    </el-card>
    <!-- 编辑用户弹窗 -->
    <!-- <el-dialog title="编辑用户" :visible.sync="dialogVisible1" width="60%" :before-close="handleClose1">
        <div id="pdfDom">
          <div class="proBox">
            <div class="chapter" v-show="isShow">
              <el-form :model="backstage_editForm" ref="backstage_editForm">
              <div class="layer03" style="margin-right: 200px">
                <span style="margin-right: 29px">用户ID :</span>{{backstage_editForm.user_id}}
              </div>
              <div class="layer03">
                <span style="margin-right: 10px">用户名字 :</span>
                <input type="text" v-model=" backstage_editForm.username" maxlength="20"/>
              </div>
              <div class="layer03">
                <span style="margin-right: 15px">电话号码 :</span>
                <input type="text" v-model=" backstage_editForm.phone" maxlength="20"/>
              </div>
              <div class="layer03">
                <span style="margin-right: 38px">密码 :</span>
                <input type="text" v-model=" backstage_editForm.password" maxlength="20"/>
              </div>
              <div class="layer03">
                <span style="margin-right: 15px">用户权限 :</span>
                <input type="text" v-model=" backstage_editForm.role" maxlength="20"/>
              </div>
              </el-form>
            </div>
          </div>
        </div>
        <span slot="footer" class="dialog-footer">
          <el-button @click="dialogVisible1 = false">取 消</el-button>
          <el-button @click="backstage_sumbit()">提交</el-button>
        </span>
      </el-dialog> -->
    <!-- 列表 -->
   <el-table
    :data=" Backstagelist"
    style="width: 100%"
    max-height="320">
    <el-table-column
      fixed
      prop="user_id"
      label="用户ID"
      width="200">
    </el-table-column>
    <el-table-column
      prop="username"
      label="用户名字"
      width="250">
    </el-table-column>
    <el-table-column
      prop="phone"
      label="电话号码"
      width="250">
    </el-table-column>
    <el-table-column
      prop="password"
      label="密码"
      width="200">
    </el-table-column>
    <el-table-column
      prop="role"
      label="权限"
      width="150">
    </el-table-column>
    <el-table-column
      fixed="right"
      label="操作"
      width="150">
      <template slot-scope="scope">
        <!-- <el-button  @click.native.prevent="edit_info(scope.$index,scope.row)"   type="text"  size="small">
          编辑
        </el-button> -->
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
  name:'certList',
    data() {
      return {
        Backstagelist:[],

        //前端测试用数据
      //   Backstagelist: [
      //   {
      //     user_id:"admin", //用户id
      //     username:"李赫海", //用户名
      //     phone:"13745678910", //电话号码
      //     password:"111", //密码
      //     role:"管理员",//权限
      //   }, 
      //   {
      //     user_id:"mini", //用户id
      //     username:"黄米妮", //用户名
      //     phone:"13910987654", //电话号码
      //     password:"222", //密码
      //     role:"普通用户",//权限
      //   }, 
      //   {
      //     user_id:"lwt223", //用户id
      //     username:"Icy", //用户名
      //     phone:"143678265490", //电话号码
      //     password:"123", //密码
      //     role:"普通用户",//权限
      //   }, 
      // ],
        backstage_SelectForm:{
          type: "",
          info: ""
        },
        //添加用户
        backstage_addForm:{
          user_id:"",
          username:"", //用户名
          phone:"", //电话号码
          password:"", //密码
          role:"",//权限
        },
        //删除用户
        backstage_delForm:{
          user_id:""
        },
        //添加框的标志值
        dialogVisible: false,
        //编辑框的标志值
        dialogVisible1: false,
        pageData: null, //接收html格式代码
        // htmlTitle: "结业证书",
        isShow: true,
      }
    },
    created(){
      this.getList();
    },
    async mounted() {
      this.BackstagelistGet();
    },
    methods:{
    //获取用户数据
    BackstagelistGet(){
      this.getRequest('http://127.0.0.1:5000/UserList').then(resp=>{
        if(resp.re_code=="0"){
          this.Backstagelist=resp.users;
        }else{
              alert(resp.msg);
              return false;
            }
      })
    },
    // 查询用户
    backstageSearch() {
      this.getRequest('http://127.0.0.1:5000/Admin',this.backstage_SelectForm).then(resp=>{
            if(resp.re_code=="0"){
              //返回搜索结果
              //刷新数据列表
              this.Backstagelist=resp.users;
            }
            else{
          this.$message.error('无该搜索结果');
          return false;
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
    // 添加新用户提交
    backstage_sumbit(){
      this.$refs.backstage_addForm.validate((valid) => {
        if(valid){
          this.postRequest('http://127.0.0.1:5000/Admin',this.backstage_addForm).then(resp=>{
            if(resp.re_code=="0"){
              alert("添加成功")
              //刷新数据列表
              this.BackstagelistGet();
              //弹窗的表单变为空值
              this.backstage_addForm.user_id="";
              this.backstage_addForm.username="";
              this.backstage_addForm.phone="";
              this.backstage_addForm.password="";
              this.backstage_addForm.role="";
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
    //编辑项目按钮
    edit_info(index, data) {
      this.backstage_editForm=data;
      this.dialogVisible1 = true;
    },
    //  //编辑用户提交
    // backstage_edit(){
    //   this.putequest('http://127.0.0.1:5000/Admin',this.backstage_editForm).then(resp=>{
    //     if(resp.re_code=="0"){
    //       //刷新数据列表
    //       this.BackstagelistGet();
    //       //关闭弹窗
    //       this.handleClose1();
    //     }
    //   })
    // },
    // 删除项目
    deleteRow(index, data) {
        // rows.splice(index, 1); //前端删除代码
        this.$confirm('此操作将永久删除['+data.username+']用户, 是否继续?', '提示', {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          this.backstage_delForm.user_id=data.user_id;
          this.deleteRequest('http://127.0.0.1:5000/Admin',this.backstage_delForm).then(resp=>{
            if(resp.re_code=="0"){
              this.$message({
              type: 'success',
              message: '删除成功!'
              });
              //刷新数据列表
              this.BackstagelistGet();
            }
          })
        }).catch(() => {
          this.$message({
            type: 'info',
            message: '已取消删除'
          });          
        });
    },
  }
}
</script>

<style lang="less">
.backstage {
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
    height:100px;
  }
        
}
</style>