<template>
  <div id="app">
    <NavigationBar />
    <router-view />
    <app-Footer />
  </div>
</template>

<script>
import NavigationBar from "./components/NavigationBar.vue";
import AppFooter from "./components/AppFooter.vue";

export default {
  components: {
    NavigationBar,
    AppFooter,
  },

  computed: {
    isLoggedIn() {
      return !!localStorage.getItem('token'); // 토큰이 있으면 로그인 상태
    },
  },
};
</script>

<style scoped>
#app {
  display: flex;
  flex-direction: column;
  min-height: 100vh; /* 화면의 높이를 채우기 위한 최소 높이 */
}
router-view {
  flex: 1; /* 메인 컨텐츠 영역이 남은 공간을 차지하도록 설정 */
}
app-footer {
  background-color: #f8f9fa;
  padding: 10px;
  text-align: center;
}
footer {
  margin-top: auto; /* Footer를 항상 아래에 고정 */
}
nav {
  display: flex;
  gap: 10px;
  background-color: #f8f9fa;
  padding: 10px;
}
button {
  background-color: #dc3545;
  color: white;
  border: none;
  padding: 5px 10px;
  cursor: pointer;
}
button:hover {
  background-color: #c82333;
}
</style>
