import JobDetail from '../views/seeker/JobDetail.vue'
import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Register from '../views/Register.vue'
import SeekerHome from '../views/seeker/SeekerHome.vue'
import SeekerDashboard from '../views/seeker/SeekerDashboard.vue'
import JobList from '../views/seeker/JobList.vue'
import MyResume from '../views/seeker/MyResume.vue'
import RecommendJobs from '../views/seeker/RecommendJobs.vue'
import MyApplications from '../views/seeker/MyApplications.vue'
import HrHome from '../views/hr/HrHome.vue'
import HrDashboard from '../views/hr/HrDashboard.vue'
import JobPublish from '../views/hr/JobPublish.vue'
import JobManage from '../views/hr/JobManage.vue'
import CandidateList from '../views/hr/CandidateList.vue'
import AdminHome from '../views/admin/AdminHome.vue'
import JobReview from '../views/admin/JobReview.vue'
import UserManage from '../views/admin/UserManage.vue'
import Stats from '../views/admin/Stats.vue'

const router = createRouter({
  history: createWebHistory(),
  routes: [
    { path: '/', component: Login },
    { path: '/register', component: Register },
    {
      path: '/seeker',
      component: SeekerHome,
      children: [
        { path: '', component: SeekerDashboard },
        { path: 'jobs', component: JobList },
        { path: 'resume', component: MyResume },
        { path: 'recommend', component: RecommendJobs },
        { path: 'applications', component: MyApplications },
        { path: 'jobs/:id', component: JobDetail },
      ]
    },
    {
      path: '/hr',
      component: HrHome,
      children: [
        { path: '', component: HrDashboard },
        { path: 'publish', component: JobPublish },
        { path: 'jobs', component: JobManage },
        { path: 'candidates', component: CandidateList },
      ]
    },
    {
      path: '/admin',
      component: AdminHome,
      children: [
        { path: '', component: Stats },
        { path: 'users', component: UserManage },
        { path: 'review', component: JobReview },
        { path: 'stats', component: Stats },
      ]
    }
  ]
})

export default router