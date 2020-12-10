import Vue from 'vue'
import axios from 'axios'
import { settings } from '../config/constants'

Vue.prototype.$axios = axios

const apiLink = settings.apiLink
const version = settings.version
// const appName = settings.appName
const compile = settings.compile

const keyToken = 'user_' + version + compile

const HTTPClient = axios.create({
  baseURL: apiLink
})
HTTPClient.defaults.withCredentials = true
HTTPClient.defaults.xsrfCookieName = 'csrftoken'
HTTPClient.defaults.xsrfHeaderName = 'X-CSRFToken'
const token = localStorage.getItem(keyToken + '-token')
if (token === null) {

} else {
  HTTPClient.defaults.headers.common.Authorization = 'Token ' + token
}

export {
  HTTPClient
}
