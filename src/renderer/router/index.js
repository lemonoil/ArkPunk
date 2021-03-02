import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'chart-page',
      component: require('@/components/VChartsBar').default
    },
    {
      path: '*',
      redirect: '/'
    }
  ]
})
