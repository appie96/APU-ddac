<template>
  <div class="not-found-container">
    <h1>404 - Page Not Found</h1>
    <p>The page you're looking for doesn't exist.</p>
    <router-link to="/" class="btn">Go Back to Home</router-link>
  </div>
</template>

<script>
export default {};
</script>

<style scoped>
.not-found-container {
  text-align: center;
  padding: 50px 20px;
}
h1 {
  font-size: 2.5rem;
  color: #dc3545;
  margin-bottom: 20px;
}
p {
  font-size: 1.2rem;
  margin-bottom: 30px;
}
.btn {
  display: inline-block;
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  text-decoration: none;
  border-radius: 5px;
}
.btn:hover {
  background-color: #0056b3;
}
</style>
