<template>
  <!-- 自定义证书详情页 -->
  <div class="design">
    <div class="title">自定义证书</div>
    <div class="huabu">
      <div class="operator-area">
        宽度：
        <input type="text" name="width" v-model="value1" class="input1" /> 
        高度：
        <input type="text" name="height" v-model="value2" class="input1" />
        <button @click="changeSize" class="button1">创建画布</button>
        <p>Tips:先创建画布再自定义设计证书</p>
        <br />
        <!-- 添加文本的按钮 -->
        <button @click="addElement(1)" :style="{ border: this.textFlag ? '1px solid blue' : '' }" class="button1">
          添加文本</button>&emsp;
        <!-- 添加线条的按钮 -->
        <button @click="addElement(2)" :style="{ border: this.lineFlag ? '1px solid blue' : '' }" class="button1">
          添加线条</button>&emsp;
          <!-- 添加图片的按钮 -->
        <button @click="addElement(3)" :style="{ border: this.imgFlag ? '1px solid blue' : '' }" class="button1">
          添加图片</button>&emsp;
        <div style="margin-top: 20px" v-if="textFlag">
          <input type="text" v-model="text" style="width: 200px; height: 50px"/>
          <button @click="addText()" class="button3">
            {{ this.textActiveIndex >= 0 ? "修改" : "添加" }}
          </button>
          <br />
          <div class="style1">
          x:
          <input type="text" name="" v-model="textPos.x" class="input" id="" />
          y:
          <input type="text" name="" v-model="textPos.y" class="input" id="" />
          字号:
          <input type="text" name="" v-model="fontSize" class="input" id="" />
          <br />
          </div>
          颜色:
          <input type="text" name="" v-model="fontColor" class="input" id="" />
          <button v-if="textActiveIndex >= 0" @click="notEditor(1)" class="button1"> 
            终止修改
          </button>
          <p>tips:点击已有文字进行编辑</p>
        </div>
        <div style="margin-top: 20px" v-if="lineFlag">
          <p>Tips:画新路径前先终止上一条路径</p>

          <button @click="notEditor(2)" class="button1">终止划线</button>
        </div>
        <div style="margin-top: 20px" v-if="imgFlag">
          <input type="file" ref="img" @change="getChange()" />
          <div
            style="
              border: 3px solid yellow;
              width: 220px;
              padding: 10px;
              margin: 20px;
              min-height: 200px;
            "
          >
            <img :src="src" alt="" style="width: 200px" />
          </div>
          <div class="style1">
            width:
            <input type="text" name="" v-model="imgSize.width" class="input" id=""/>
            height:
            <input type="text"  name=""  v-model="imgSize.height"  class="input"  id=""  />
          </div>
          x:
          <input type="text" name="" v-model="imgPos.x" class="input" id="" />
          y:
          <input type="text" name="" v-model="imgPos.y" class="input" id="" />
          <button @click="addImg()" class="button1">添加图片</button>
          <p>Tips:可通过拖拽改变图片位置</p>
        </div>
        <hr />
        <br>
         <button @click="reserve" class="button2">保存证书</button>
        <button @click="download" class="button2">下载证书</button>
      </div>
      <div class="show-area">
        <v-stage :config="canvasData.stage" @mousedown="drawLine" ref="stage">
          <v-layer>
            <v-image
              @dragend="dragEvent($event, index)"  :config="imgConfig"
              v-for="(imgConfig, index) in canvasData.imgs"  :key="imgConfig.id"
            ></v-image>
            <v-text
              @mousedown="textEditor($event, index)"  :config="textConfig"
              v-for="(textConfig, index) in canvasData.texts"  :key="textConfig.id"
            ></v-text>
            <v-path
              :config="lineConfig"
              v-for="lineConfig in canvasData.lines"  :key="lineConfig.id"
            ></v-path>
          </v-layer>
        </v-stage>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  // name: "certList",
  components: {},
  data() {
    return {
      // 证书ID
      certficate: {
        id: "",
      },
      text: "",
      value1: 500,
      value2: 600,
      textFlag: false,
      textActiveIndex: -1,
      textPos: { x: 100, y: 100 },
      imgPos: { x: 100, y: 100 },
      imgSize: { width: 200, height: 200 },
      fontSize: 20,
      fontColor: "red",
      lineFlag: false,
      lineData: "100,200,200,100",
      pathPoints: [],
      imgFlag: false,
      lineActiveIndex: 0,
      imgActiveIndex: -1,
      onloadImgsNum: 0,
      src: "",
      canvasData: {
        stage: {
          width: 0,
          height: 0,
        },
        texts: [],
        lines: [],
        imgs: [],
        imgList: [],
      },

      //模拟已存在模板（覆盖可以复原）
      oldCanvasData: {},
    };
  },
  mounted() {
    document.querySelector("canvas").style.border = "1px solid blue";
    // this.certficate.id=window.sessionStorage.getItem('design_id');
    
  },
  created() {
    if (!this.oldCanvasData.imgList) {
      return;
    }
    this.oldCanvasData.imgList.forEach((item, index) => {
      let img = new Image();
      img.src = item;
      img.onload = () => {
        this.oldCanvasData.imgs[index].image = img;
        this.onloadImgsNum += 1;
      };
    });
  },
  watch: {
    onloadImgsNum: {
      immediate: true,
      deep: true,
      handler(nV) {
        if (
          nV ==
          (this.oldCanvasData.imgList && this.oldCanvasData.imgList.length)
        ) {
          this.canvasData = this.oldCanvasData;
        }
      },
    },
  },
  methods: {
    textEditor(e, index) {
      this.textActiveIndex = index;
      let { x, y, fill, fontSize } = e.target.attrs;
      this.textPos = { x, y };
      this.fontColor = fill;
      this.fontSize = fontSize;
    },
    dragEvent(e, index) {
      let { width, height, x, y, draggable, image } = e.target.attrs;
      this.canvasData.imgs.splice(index, 1, {
        width,
        height,
        x,
        y,
        draggable,
        image,
      });
    },
    reserve(){
      this.$refs.canvasData.validate((valid) => {
        if(valid){
          this.postRequest('http://127.0.0.1:5000/certficate',this.canvasData).then(resp=>{
            if(resp){
              alert("保存成功")
            }else{
                  alert(resp.msg);
                  return false;
                }
          })
        }
      })
    },
    download() {
      let canvas = document.querySelector("canvas");
      let base64 = canvas.toDataURL("image/png");
      let a = document.createElement("a");
      a.download = new Date().getTime();
      a.href = base64;
      a.click();
      this.canvasData.imgList = this.canvasData.imgs.map((item) => {
        return item.image.src;
      });
      console.log("模拟json数据", this.canvasData);
    },
    getChange() {
      let dom = this.$refs.img.files[0];
      let reader = new FileReader();
      reader.readAsDataURL(dom);
      reader.onload = (result) => {
        this.src = result.target.result;
      };
    },
    //画线
    drawLine() {
      if (this.lineFlag) {
        let data = "";
        let position = this.$refs.stage.getNode().getPointerPosition();
        this.pathPoints.push(position.x);
        this.pathPoints.push(position.y);
        for (let index = 0; index < this.pathPoints.length; index += 2) {
          if (index == 0) {
            data += `M${this.pathPoints[index]} ${this.pathPoints[index + 1]} `;
          } else if (index == this.pathPoints.length - 2) {
            data += `L${this.pathPoints[index]} ${this.pathPoints[index + 1]} `;
          } else {
            data += `L${this.pathPoints[index]} ${this.pathPoints[index + 1]} `;
          }
        }
        let obj = {
          x: 0,
          y: 0,
          stroke: "blue",
          strokeWidth: 3,
          data,
        };
        if (this.lineActiveIndex == 0) {
          this.canvasData.lines.push(obj);
        } else {
          this.canvasData.lines.splice(this.lineActiveIndex, 1, obj);
        }
      }
    },
    notEditor(num) {
      if (num == 1) {
        this.textActiveIndex = -1;
      } else if (num == 2) {
        this.lineActiveIndex = this.canvasData.lines.length;
        this.canvasData.lines.push({});
        this.pathPoints = [];
        this.lineFlag = false;
      }
    },
    // 添加图片
    addImg() {
      let index = this.canvasData.imgs.length;
      let img = new Image();
      img.src = this.src;
      img.onload = () => {
        this.canvasData.imgs[index].image = img;
      };
      let obj = {
        x: Number(this.imgPos.x),
        y: Number(this.imgPos.y),
        width: Number(this.imgSize.width),
        height: Number(this.imgSize.height),
        image: null,
        draggable: true,
      };
      this.canvasData.imgs.push(obj);
    },
    // 添加文本
    addText() {
      let obj = {
        x: Number(this.textPos.x),
        y: Number(this.textPos.y),
        text: this.text,
        fontSize: this.fontSize,
        fill: this.fontColor,
      };
      if (this.textActiveIndex >= 0) {
        this.canvasData.texts.splice(this.textActiveIndex, 1, obj);
        return;
      }
      this.canvasData.texts.push(obj);
      this.textActiveIndex = this.canvasData.texts.length - 1;
    },
    //选择工具
    addElement(num) {
      this.lineFlag = false;
      this.imgFlag = false;
      this.textFlag = false;
      this.lineActiveIndex = -1;
      this.textActiveIndex = -1;
      this.imgActiveIndex = -1;
      if (num == 1) {
        this.textFlag = true;
      } else if (num == 2) {
        this.lineFlag = true;
      } else if (num == 3) {
        this.imgFlag = true;
      }
    },
    //画布大小
    changeSize() {
      this.canvasData.stage.width = Number(this.value1);
      this.canvasData.stage.height = Number(this.value2);
    },
  },
};
</script>

<style lang="less">
.design {
  .title {
    font-size: 18px;
    font-weight: 700;
  }
  .operator-area {
    width: 315px;
    height: 500px;
    border-right: 1px solid black;
    top: 100px;
    left: 10px;
  }
  .show-area {
    width: 800px;
    height: 600px;
    position: absolute;
    top: 75px;
    left: 550px;
  }
  .input {
    width: 40px;
    height: 28px;
    outline: none;
    border:#0668bc 1px solid;
    margin-right: 10px;
  }
  .input1 {
    width: 40px;
    height: 28px;
    outline: none;
    border:#0668bc 1px solid;
    // margin-right: 10px;
  }
  .huabu{
    margin-top: 25px;
  }
  .button1{
    width:78px;
    height:36px;
    background-color:#0668bc;;
    color:white;
    border-radius: 8px;
    border:0px;
    margin-left: 10px;
  }
  .button2{
    width:100px;
    height:36px;
    background-color:#0668bc;;
    color:white;
    border-radius: 8px;
    border:0px;
    margin-left: 10px;
  }
  .button3{
    width:60px;
    height:36px;
    background-color:#0668bc;;
    color:white;
    border-radius: 8px;
    border:0px;
    margin-left: 10px;
  }
  .style1{
    margin:15px 0px;
  }
}
</style>