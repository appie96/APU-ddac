import { createApp, reactive } from 'vue';
import App from './App.vue';
import router from './router';
import axios from 'axios';
import "bootstrap/dist/css/bootstrap.min.css";
import "bootstrap/dist/js/bootstrap.bundle.min";

axios.defaults.baseURL = process.env.VUE_APP_BASE_URL; // .env에서 API 기본 URL 가져오기

const app = createApp(App);
const appState = reactive({
  isLoggedIn: !!localStorage.getItem("token"), // 초기 로그인 상태 설정
  user: JSON.parse(localStorage.getItem("user")) || {}, // 사용자 정보 저장
  isSuperuser: false // superuser 상태 추가
});

// Vue 전역 속성 추가
app.config.globalProperties.$isLoggedIn = () => {
  // localStorage에 토큰이 있는지 확인하여 로그인 상태 반환
  return !!localStorage.getItem("token"); 
};

app.config.globalProperties.$isSuperuser = () => {
  // JWT 토큰의 payload를 디코드하여 superuser 여부 반환
  const token = localStorage.getItem("token");
  if (token) {
    try {
      const payload = JSON.parse(atob(token.split(".")[1])); // JWT payload 추출
      return payload.is_superuser || false; // superuser 필드 반환
    } catch (error) {
      console.error("Error decoding token:", error);
      return false;
    }
  }
  return false; // 토큰이 없으면 false 반환
};

app.config.globalProperties.$logout = () => {
  localStorage.removeItem("token");
  localStorage.removeItem("user");
  appState.isLoggedIn = false;
  appState.user = {};
  appState.isSuperuser = false;
};

// 전역 함수 추가
window.isLoggedIn = app.config.globalProperties.$isLoggedIn;
window.isSuperuser = app.config.globalProperties.$isSuperuser;
window.logout = app.config.globalProperties.$logout;

app.provide("appState", appState);
app.use(router);
app.config.globalProperties.$axios = axios;
app.mount('#app');

// 로그인 상태가 변경될 때마다 superuser 상태를 업데이트
if (appState.isLoggedIn) {
  appState.isSuperuser = app.config.globalProperties.$isSuperuser();
}
