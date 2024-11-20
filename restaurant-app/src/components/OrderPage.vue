<template>
  <div class="order-page">
    <h1>Order {{ menu.name }}</h1>
    <img :src="menu.image_url" alt="menu image" />
    <p>{{ menu.description }}</p>
    <p>Price: ${{ menu.price }}</p>
    <!-- Add your order form here -->
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
    const menuId = this.$route.params.id;
    axios
      .get(`https://gy3d55i8pc.execute-api.us-east-1.amazonaws.com/menu/${menuId}`)
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
.order-page {
  text-align: center;
  padding: 20px;
}
.order-page img {
  max-width: 300px;
  margin: 20px 0;
}
</style>