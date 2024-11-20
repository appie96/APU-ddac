<template>
  <div class="menu-detail">
    <h1>{{ menu.name }}</h1>
    <img :src="menu.image_url" alt="menu image" />
    <p>{{ menu.description }}</p>
    <p>Price: ${{ menu.price }}</p>
    <router-link to="/menu" class="btn">Back to Menu</router-link>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      menu: {}
    };
  },
  mounted() {
    const menuId = this.$route.params.id; // URL에서 메뉴 ID 가져오기
    axios
      .get(`https://your-api-url/menu/${menuId}`) // 실제 API URL 사용
      .then(response => {
        this.menu = response.data;
      })
      .catch(error => {
        console.error('Error fetching menu details:', error);
      });
  }
};
</script>

<style scoped>
.menu-detail {
  text-align: center;
  padding: 20px;
}
.menu-detail img {
  max-width: 300px;
  margin: 20px 0;
}
</style>
