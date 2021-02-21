import Vue from 'vue'
import axios from 'axios'

import App from './App'
import router from './router'
import store from './store'
import Element from 'element-ui'

import VeLine from 'v-charts/lib/line.common'
import VeBar from 'v-charts/lib/bar.common'
import 'element-ui/lib/theme-chalk/index.css'

if (!process.env.IS_WEB) Vue.use(require('vue-electron'))
Vue.http = Vue.prototype.$http = axios
Vue.config.productionTip = false



// Vue.use(new VueSocketIO({
//   debug: true,
//   connection: 'http://127.0.0.1:4242',
//   vuex: {
//     store,
//     actionPrefix: 'SOCKET_',
//     mutationPrefix: 'SOCKET_'
//   },

// }))

Vue.use(Element)
Vue.component(VeLine.name, VeLine)
Vue.component(VeBar.name, VeBar)
new Vue({
  el: '#app',
  render: h => h(App),
  router,
  store
});

