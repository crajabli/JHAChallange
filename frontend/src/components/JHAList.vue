<template>
    <div class="container mt-5">
   <div class="d-flex justify-content-between align-items-center mb-3">
     <h1>Job Hazard Analysis</h1>
     <router-link to="/jha/add" class="btn btn-primary">+ Add JHA</router-link>
   </div>

   <table class="table table-hover">
     <thead class="table-dark">
       <tr>
         <th>Title</th>
         <th>Author</th>
         <th>Last Updated</th>
       </tr>
     </thead>
     <tbody>
       <tr v-for="jha in jhas" :key="jha.id" @click="editJHA(jha.id)" class="cursor-pointer">
         <td>{{ jha.title }}</td>
         <td>{{ jha.author }}</td>
         <td>{{ formatDate(jha.updated_at) }}</td>
       </tr>
     </tbody>
   </table>
 </div>
</template>

<script>
   import { ref, onMounted } from 'vue'
   import { useRouter } from 'vue-router'
    import axios from 'axios'

   export default {
       name: 'JHAList',
       setup() {
           const jhas = ref([])
           const router = useRouter()

           const fetchJHAs = async () => {
               try {
                   const response = await axios.get('/jhas')
                   jhas.value = response.data.jhas
               } catch (error) {
                   console.error('Error fetching JHAs', error)
               }
           }

           const editJHA = (id) => {
               router.push({ name: 'EditJHA', params: { id } })
           }

           const formatDate = (date) => {
               return new Date(date).toLocaleDateString()
           }

           onMounted(fetchJHAs)

           return {
               jhas,
               editJHA,
               formatDate
           }
       }
   }
</script>

<style scoped>
.cursor-pointer {
 cursor: pointer;
}
</style>