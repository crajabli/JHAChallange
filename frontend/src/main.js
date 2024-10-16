import { createApp } from 'vue'
import App from './App.vue'
import axios from 'axios'
import router from './router'
import 'bootstrap/dist/css/bootstrap.min.css'
import 'bootstrap/dist/js/bootstrap.min.js'

const app = createApp(App)

axios.defaults.baseURL = 'http://localhost:5000'

app.config.globalProperties.$axios = axios

app.use(router)
app.mount('#app')
