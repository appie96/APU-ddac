<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <h2 class="text-center mb-4">Login</h2>
        <form @submit.prevent="loginUser">
          <div class="mb-3">
            <label for="email" class="form-label">Email address</label>
            <input
              type="email"  
              id="email"
              v-model="email"
              class="form-control"
              placeholder="Enter your email"  
              required
              :disabled="isLoading"
            />
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input
              type="password"
              id="password"
              v-model="password"
              class="form-control"
              required
              :disabled="isLoading"
            />
          </div>
          <button 
            type="submit" 
            class="btn btn-primary w-100"
            :disabled="isLoading"
          >
            {{ isLoading ? 'Logging in...' : 'Login' }}
          </button>
        </form>
        <div v-if="errorMessage" class="alert alert-danger mt-3">
          {{ errorMessage }}
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { inject, ref } from "vue";
import axios from "axios";
import { useRouter } from "vue-router";

export default {
  name: 'LoginPage',
  setup() {
    const appState = inject("appState");
    const router = useRouter();
    
    const email = ref("");
    const password = ref("");
    const errorMessage = ref("");
    const isLoading = ref(false);

    const loginUser = async () => {
      try {
        errorMessage.value = "";
        isLoading.value = true;

        const response = await axios.post(
          "http://127.0.0.1:8000/api/login", 
          {
            email: email.value,
            password: password.value
          },
          {
            headers: {
              'Content-Type': 'application/json'
            }
          }
        );

        if (response.data && response.data.access) {
          localStorage.setItem('token', response.data.access);
          axios.defaults.headers.common['Authorization'] = `Bearer ${response.data.access}`;
          appState.isLoggedIn = true;
          router.push('/');
        }
      } catch (error) {
        console.error("Login error:", error.response?.data);
        errorMessage.value = 
          error.response?.data?.error || 
          error.response?.data?.detail || 
          "Login failed. Please try again.";
      } finally {
        isLoading.value = false;
      }
    };

    return {
      email,
      password,
      errorMessage,
      isLoading,
      loginUser
    };
  }
}
</script>

<style scoped>
.container {
  max-width: 800px;
}
</style>
