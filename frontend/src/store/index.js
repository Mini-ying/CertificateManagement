import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    asideType: 1,
    obj: {},
    inputValue: null
  },
  mutations: {
    setAsideType (state, payload) {
      state.asideType = payload
    },
    setObj (state, payload) {
      state.obj = {...payload}
    },
    // 存储输入的值
    setInputValue (state, payload) {
      state.inputValue = payload
    },
  },
  actions: {
  },
  modules: {
  }
})
