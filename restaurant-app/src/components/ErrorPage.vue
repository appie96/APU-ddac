<template>
  <div class="error-page">
    <h1>404 - Page Not Found</h1>
    <p>The page you are looking for doesn't exist.</p>
    <router-link to="/">Go Back to Home</router-link>
  </div>
</template>

<script>
export default {
  name: "ErrorPage",
};
</script>

<style>
.error-page {
  text-align: center;
  margin-top: 50px;
}

.error-page h1 {
  font-size: 48px;
  color: red;
}

.error-page p {
  font-size: 18px;
}

.error-page a {
  display: inline-block;
  margin-top: 20px;
  padding: 10px 20px;
  background-color: #007bff;
  color: #fff;
  text-decoration: none;
  border-radius: 5px;
}

.error-page a:hover {
  background-color: #0056b3;
}
</style>
