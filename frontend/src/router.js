import { createRouter, createWebHistory } from 'vue-router'
import JHAList from './components/JHAList.vue'
import JHAForm from './components/JHAForm.vue'
import StepForm from './components/StepForm.vue'


const routes = [
    {path: '/', name:'JHAList', component: JHAList},
    {path: '/jha/add', name:'AddJHA', component: JHAForm},
    {path: '/jha/:id', name:'EditJHA', component: JHAForm, props: true},
    {path: '/jha/:jhaId/step/add', name:'AddStep', component: StepForm, props: true},
    {path: '/jha/:jhaId/step/:stepId', name:'EditStep', component: StepForm, props: true},
]

const router = createRouter({
    history: createWebHistory(),
    routes, 
})

export default router