import { createRouter, createWebHistory } from 'vue-router';
import HomePage from '../components/HomePage.vue';
import MenuList from '../components/MenuList.vue';
import ReservationPage from '../components/ReservationPage.vue';
import ReservationEdit from '../components/ReservationEdit.vue';
import ReservationConfirm from '../components/ReservationConfirm.vue';
import ReservationCancel from '../components/ReservationCancel.vue';
import LoginPage from '../components/LoginPage.vue';
import ProfilePage from '../components/ProfilePage.vue';
import AdminPage from '../components/AdminPage.vue';
import NotFound from '../components/NotFound.vue';

const routes = [
  { path: '/', name: 'Home', component: HomePage },
  { path: '/menu', name: 'Menu', component: MenuList },
  { path: '/reservation', name: 'Reservation', component: ReservationPage },
  { path: '/reservation/edit', name: 'ReservationEdit', component: ReservationEdit },
  { path: '/reservation/confirm', name: 'ReservationConfirm', component: ReservationConfirm },
  { path: '/reservation/cancel', name: 'ReservationCancel', component: ReservationCancel },
  { path: '/login', name: 'Login', component: LoginPage },
  { path: '/profile', name: 'Profile', component: ProfilePage },
  { path: '/admin', name: 'Admin', component: AdminPage },
  { path: '/:pathMatch(.*)*', name: 'NotFound', component: NotFound },
];

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes,
});

export default router;
