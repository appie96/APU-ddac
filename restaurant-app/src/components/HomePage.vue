<template>
  <div class="home-container">
    <h1>Welcome to Our Restaurant</h1>
    <p>Experience the finest dining with us. Check out our menu or make a reservation today!</p>
    <div class="home-buttons">
      <router-link to="/menu" class="btn">View Menu</router-link>
      <router-link to="/reservation" class="btn">Make a Reservation</router-link>
    </div>
  </div>
</template>

<script>
export default {};
</script>

<style scoped>
.home-container {
  text-align: center;
  padding: 50px 20px;
}
h1 {
  font-size: 2.5rem;
  margin-bottom: 20px;
}
p {
  font-size: 1.2rem;
  margin-bottom: 30px;
}
.home-buttons .btn {
  display: inline-block;
  margin: 0 10px;
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  text-decoration: none;
  border-radius: 5px;
}
.home-buttons .btn:hover {
  background-color: #0056b3;
}
</style>
