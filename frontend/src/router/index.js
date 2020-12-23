import Vue from 'vue'
import VueRouter from 'vue-router'

import routes from './routes'

Vue.use(VueRouter)

import VueApexCharts from 'vue-apexcharts'
Vue.use(VueApexCharts)
try {
  var GoogleMapsKey = require('boot/secret')
  console.log('GoogleMapsKey Externa')

  console.log(GoogleMapsKey.GoogleMapsKey)
} catch (e) {
  const GoogleMapsKey = { GoogleMapsKey: 'INSIRA SUA KEY' }
  console.log('GoogleMapsKey Interna')
  console.log(GoogleMapsKey)
}

import VueGoogleHeatmap from 'vue-google-heatmap'

Vue.use(VueGoogleHeatmap, {
  apiKey: GoogleMapsKey.GoogleMapsKey
})
Vue.component('apexchart', VueApexCharts)
import { library } from '@fortawesome/fontawesome-svg-core'
import { faUserSecret } from '@fortawesome/free-solid-svg-icons'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(faUserSecret)

Vue.component('font-awesome-icon', FontAwesomeIcon)

/*
 * If not building with SSR mode, you can
 * directly export the Router instantiation;
 *
 * The function below can be async too; either use
 * async/await or return a Promise which resolves
 * with the Router instance.
 */

export default function (/* { store, ssrContext } */) {
  const Router = new VueRouter({
    scrollBehavior: () => ({ x: 0, y: 0 }),
    routes,

    // Leave these as they are and change in quasar.conf.js instead!
    // quasar.conf.js -> build -> vueRouterMode
    // quasar.conf.js -> build -> publicPath
    mode: process.env.VUE_ROUTER_MODE,
    base: process.env.VUE_ROUTER_BASE
  })

  return Router
}
