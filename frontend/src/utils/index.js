/**
 * 获取侧边栏，并转化为一维结构
 * */ 
export let getDatasOptions = async () => {
  let datas = () => {
    return import('@/utils/datas.json')
  }
  // JSON.parse(JSON.stringify()) 最简单的深拷贝
  // await 可以获取到promise中resolve、reject的值
  let datasJson = JSON.parse(JSON.stringify(await datas())).default
  let datasOption = []
  let getDataOptions = (data) => {
    if (data && data.length) {
      for (let i in data) {
        datasOption.push({
          id: data[i].id,
          label: data[i].label
        })
        // 调用自己，递归函数
        getDataOptions(data[i].children)
      }
    }
  }
  getDataOptions(datasJson)
  return datasOption
}