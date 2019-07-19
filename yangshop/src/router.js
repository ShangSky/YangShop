import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

export default new Router({
  // mode: 'history',
  routes: [
    { path: '/', component: () => import('./views/goods/index.vue') },
    { path: '/type/:id', component: () => import('./views/goods/type.vue') },
    { path: '/search', component: () => import('./views/goods/search.vue') },
    { path: '/detail/:goodsId', component: () => import('./views/goods/detail.vue') },

    { path: '/cart', component: () => import('./views/trade/cart.vue') },
    { 
      path: '/orders', 
      component: () => import('./views/trade/orders.vue'),
      children: [
        {path: 'info', component: ()=> import('./views/trade/orderInfo.vue')},
        {path: 'comments', component: ()=> import('./views/trade/comments.vue')},
      ]
    },
    {
      path: '/user', 
      component: () => import('./views/user/user.vue'), 
      children: [
        {path: 'fav', component: ()=> import('./views/user/userFav.vue')},
        {path: 'account', component: ()=> import('./views/user/account.vue')},
        {path: 'address', component: ()=> import('./views/user/address.vue')},
        {path: 'address/add', component: ()=> import('./views/user/addressAdd.vue')},
        {path: 'address/edit/:id', component: ()=> import('./views/user/addressEdit.vue')}
      ]
    },
    
    { path: '/login', component: () => import('./views/account/login.vue') },
    { path: '/register', component: () => import('./views/account/register.vue') },
    { path: '/pwd', component: () => import('./views/account/pwd.vue') },

    { path: '/*', redirect: '/' },
  ]
})
