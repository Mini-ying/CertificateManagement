<template>
<!-- 项目管理详情页 -->
  <div class="sessions" >
    <el-table
        :data="tableData3"
        border
        id="el-table"
        style="width: 100%">
        <!-- 动态循环的列表 -->
        <template  v-for="(item, index) in tableLabel">
          <el-table-column
            :key="index"
            :prop="item.prop"
            :label="item.label"
            width="">
          </el-table-column>
        </template>
        <!-- 固定的列：从业人员 -->
        <el-table-column label="从业人员">
          <template slot-scope={}>
            <el-button type="info" >从业人员</el-button>
            </template>
        </el-table-column>        
      </el-table>
  </div>
</template>

<script>
export default {
  name: "dataList",
  data() {
    return {
      tableData3: [
        {
          id: '1',
          number: '112',
          a: '这是个数据',
          b: '这是个数据'
        }, {
          id: '2',
          number: '113',
          a: '这是个数据',
          b: '这是个数据'
        }
      ],
      tableLabel: [
          {label: '序号', prop: 'id'},
          {label: '场所编号', prop: 'number'},
          {label: '表头3', prop: 'a'},
          {label: '表头4', prop: 'b'},
      ]
    }
  },
}
</script>
