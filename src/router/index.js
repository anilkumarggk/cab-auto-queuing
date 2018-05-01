import Vue from 'vue'
import Router from 'vue-router'
import Landing from '../components/Landing'
import UserApp from '../components/UserApp'
import DriverApp from '../components/DriverApp'
import Dashboard from '../components/Dashboard'
import GlobalNavBar from '../components/GlobalNavBar'

Vue.use(Router)

// Re-usabel component definitions:
Vue.component('GlobalNavBar', GlobalNavBar)

export default new Router({
    routes: [
        {
            path: '/',
            name: 'Landing',
            component: Landing,
            nav: {
                visible: true,
                title: 'Home'
            }
        }, {
            path: '/user/:user_id?',
            name: 'UserApp',
            component: UserApp,
            nav: {
                visible: true,
                title: 'User App'
            }
        }, {
            path: '/driver/:driver_id?',
            name: 'DriverApp',
            component: DriverApp,
            nav: {
                visible: true,
                title: 'Driver App'
            }
        }, {
            path: '/dashboard',
            name: 'Dashboard',
            component: Dashboard,
            nav: {
                visible: true,
                title: 'Dashboard'
            }
        }
    ],
    mode: 'history'
})
