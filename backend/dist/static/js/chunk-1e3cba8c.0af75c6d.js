(window["webpackJsonp"]=window["webpackJsonp"]||[]).push([["chunk-1e3cba8c"],{1795:function(e,t,i){},3817:function(e,t,i){"use strict";i.r(t);var a=function(){var e=this,t=e.$createElement,i=e._self._c||t;return i("div",{staticClass:"certificate"},[i("div",{staticClass:"title"},[i("span",{on:{click:e.reback}},[e._v(e._s(e.Project.project_name)+"项目")])]),i("el-card",{staticClass:"filter-container",attrs:{shadow:"never"}},[i("div",[i("i",{staticClass:"el-icon-search"}),i("span",[e._v("筛选搜索")]),i("el-button",{staticStyle:{float:"right"},attrs:{type:"primary",size:"small"},on:{click:function(t){return e.Search()}}},[e._v(" 查询搜索 ")]),i("el-button",{staticStyle:{float:"right","margin-right":"15px"},attrs:{size:"small"},on:{click:function(t){return e.ResetSearch()}}},[e._v(" 重置 ")])],1),i("div",{staticStyle:{"margin-top":"15px"}},[i("el-form",{attrs:{inline:!0,model:e.listQuery,size:"small","label-width":"140px"}},[i("el-form-item",{attrs:{label:"输入搜索："}},[i("select",{directives:[{name:"model",rawName:"v-model",value:e.select.selected,expression:"select.selected"}],staticClass:"select1",on:{change:function(t){var i=Array.prototype.filter.call(t.target.options,(function(e){return e.selected})).map((function(e){var t="_value"in e?e._value:e.value;return t}));e.$set(e.select,"selected",t.target.multiple?i:i[0])}}},[i("option",{attrs:{disabled:"",value:""}},[e._v("请选择")]),i("option",{attrs:{value:"sessions"}},[e._v("届次")]),i("option",{attrs:{value:"certificate_id"}},[e._v("证书编号")]),i("option",{attrs:{value:"certificate_name"}},[e._v("证书名称")]),i("option",{attrs:{value:"winner"}},[e._v("获奖者名称")]),i("option",{attrs:{value:"level"}},[e._v("证书级别")]),i("option",{attrs:{value:"datt"}},[e._v("获奖日期")]),i("option",{attrs:{value:"rank"}},[e._v("获奖名次")]),i("option",{attrs:{value:"giver"}},[e._v("颁奖机构")])]),i("el-input",{staticClass:"input-width",model:{value:e.select.selected_value,callback:function(t){e.$set(e.select,"selected_value",t)},expression:"select.selected_value"}})],1)],1)],1)]),i("el-card",{staticClass:"operate-container",attrs:{shadow:"never"}},[i("i",{staticClass:"el-icon-tickets"}),i("span",[e._v("数据列表")]),i("el-button",{staticClass:"button1",on:{click:e.add_cert}},[e._v("添加证书")])],1),i("el-table",{staticStyle:{width:"100%"},attrs:{data:e.Pro_certificate,border:"",id:"el-table"}},[e._l(e.tableLabel,(function(e,t){return[i("el-table-column",{key:t,attrs:{prop:e.prop,label:e.label,width:""}})]})),i("el-table-column",{attrs:{label:"操作"},scopedSlots:e._u([{key:"default",fn:function(t){return[i("el-button",{on:{click:function(i){return e.preview(t.row.sessions,t.row.certificate_id,t.row.certificate_name,t.row.winner,t.row.level,t.row.date,t.row.rank,t.row.giver)}}},[e._v("查看证书")]),i("el-dialog",{attrs:{title:"",visible:e.dialogVisible,width:"60%","before-close":e.handleClose},on:{"update:visible":function(t){e.dialogVisible=t}}},[i("div",{attrs:{id:"pdfDom"}},[i("div",{directives:[{name:"show",rawName:"v-show",value:e.isShow,expression:"isShow"}],staticClass:"chapter"},[i("div",{ref:"imageDom",staticClass:"proBox"},[i("p",{staticClass:"tit"},[e._v("获奖证书")]),i("p",{staticClass:"proid"},[i("span",[e._v("编号：")]),e._v(" "),i("span",[e._v(e._s(e.cert.certificate_id))])]),i("p",{staticClass:"con"},[i("span",{staticClass:"con-name"},[e._v(e._s(e.cert.winner))]),e._v(" 于"),i("span",{staticStyle:{margin:"10px"}},[e._v(e._s(e.cert.sessions))]),e._v(" “"+e._s(e.cert.certificate_name)+"” 荣获"+e._s(e.cert.level)+e._s(e.cert.rank)+" ")]),i("p",{staticClass:"con"},[e._v("特发此证,予以鼓励")]),i("div",{staticClass:"con-unit"},[i("p",[e._v(e._s(e.cert.giver))]),i("p",{staticClass:"time"},[e._v(e._s(e.cert.date))])])])])]),i("span",{staticClass:"dialog-footer",attrs:{slot:"footer"},slot:"footer"},[i("el-button",{on:{click:function(t){e.dialogVisible=!1}}},[e._v("关 闭")])],1)]),i("el-button",{on:{click:function(i){return e.delete_cert(t.row.project_id)}}},[e._v("删除")])]}}])})],2)],1)},s=[],r=i("1da1"),c=(i("96cf"),{pageNum:1,pageSize:10,id:null,receiverKeyword:null,status:null,createTime:null,handleMan:null,handleTime:null}),n={name:"pro_certList",data:function(){return{Pro_certificate:[{sessions:"第一届",certificate_id:"123",certificate_name:"abc",winner:"力大仙",level:"国家级",date:"2020.1.1",rank:"第一名",giver:"深圳技术大学"},{sessions:"第一届",certificate_id:"234",certificate_name:"abc",winner:"力大仙",level:"国家级",date:"2020.1.1",rank:"第一名",giver:"深圳技术大学"}],tableLabel:[{label:"届次",prop:"sessions"},{label:"证书编号",prop:"certificate_id"},{label:"证书名称",prop:"certificate_name"},{label:"获奖者名称",prop:"winner"},{label:"证书级别",prop:"level"},{label:"获奖日期",prop:"date"},{label:"获奖名次",prop:"rank"},{label:"颁奖机构",prop:"giver"}],UserInfo:{id:""},Project:{project_id:"",project_name:""},select:{selected:"",selected_value:""},cert:{sessions:"",certificate_id:"",certificate_name:"",winner:"",level:"",date:"",rank:"",giver:""},dialogVisible:!1,pageData:null,htmlTitle:"结业证书",isShow:!0,isCanvas:!1}},created:function(){this.getList()},mounted:function(){var e=this;return Object(r["a"])(regeneratorRuntime.mark((function t(){return regeneratorRuntime.wrap((function(t){while(1)switch(t.prev=t.next){case 0:e.UserInfo.id=e.$route.query.id,e.Project.project_id=e.$route.query.project_id,e.Project.project_name=e.$route.query.project_name;case 3:case"end":return t.stop()}}),t)})))()},methods:{getdata:function(){axios.get("http://127.0.0.1:8000/pro_cert").then((function(e,t,i,a,s,r,c,n){this.Certificate.sessions=e,this.Certificate.certificate_id=t,this.Certificate.certificate_name=i,this.Certificate.winner=a,this.Certificate.level=s,this.Certificate.date=r,this.Certificate.rank=c,this.Certificate.giver=n}))},Search:function(){axios.post("http://127.0.0.1:8000/project",{type:this.select.selected,info:this.select.selected_value}).then((function(e){console.log(e.status),0===parseInt(e.status)||alert("无该信息")}))},ResetSearch:function(){this.listQuery=Object.assign({},c)},handleClose:function(){this.dialogVisible=!1,this.cert.sessions="",this.cert.certificate_id="",this.cert.certificate_name="",this.cert.winner="",this.cert.level="",this.cert.date="",this.cert.rank="",this.cert.giver=""},preview:function(e,t,i,a,s,r,c,n){this.dialogVisible=!0,this.cert.sessions=e,this.cert.certificate_id=t,this.cert.certificate_name=i,this.cert.winner=a,this.cert.level=s,this.cert.date=r,this.cert.rank=c,this.cert.giver=n},delete_cert:function(){axios.post("http://127.0.0.1:8000/pro_cert",{certificate_id:certificate_id}),alert("删除成功")},reback:function(){this.$router.push({path:"/project:id",query:{id:this.UserInfo.id}})},check_cert:function(e){this.cert.sessions=e},add_cert:function(){this.$router.push({path:"/addcert:id,project_id,project_name",query:{id:this.UserInfo.id,project_id:this.Project.project_id,project_name:this.Project.project_name}})}}},l=n,o=(i("cc06"),i("2877")),u=Object(o["a"])(l,a,s,!1,null,null,null);t["default"]=u.exports},cc06:function(e,t,i){"use strict";i("1795")}}]);
//# sourceMappingURL=chunk-1e3cba8c.0af75c6d.js.map