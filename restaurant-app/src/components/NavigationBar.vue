<template>
  <nav class="navbar navbar-expand-lg navbar-light bg-light">
    <div class="container-fluid">
      <a class="navbar-brand" href="/">Restaurant</a>
      <button
        class="navbar-toggler"
        type="button"
        data-bs-toggle="collapse"
        data-bs-target="#navbarNav"
        aria-controls="navbarNav"
        aria-expanded="false"
        aria-label="Toggle navigation"
      >
        <span class="navbar-toggler-icon"></span>
      </button>
      <div class="collapse navbar-collapse" id="navbarNav">
        <ul class="navbar-nav ms-auto">
          <li class="nav-item">
            <router-link class="nav-link" to="/">Home</router-link>
          </li>
          <li class="nav-item">
            <router-link class="nav-link" to="/menu">Menu</router-link>
          </li>
          <li class="nav-item" v-if="appState.isLoggedIn">
            <router-link class="nav-link" to="/reservation">Reservation</router-link>
          </li>
          <li class="nav-item" v-if="appState.isLoggedIn">
            <router-link class="nav-link" to="/profile">Profile</router-link>
          </li>
          <li class="nav-item" v-if="appState.isSuperuser">
            <router-link class="nav-link" to="/admin">Admin</router-link>
          </li>
          <li class="nav-item" v-if="appState.isLoggedIn">
            <button class="btn btn-link nav-link" @click="logout">Logout</button>
          </li>
          <li class="nav-item" v-else>
            <router-link class="nav-link" to="/login">Login</router-link>
          </li>
        </ul>
      </div>
    </div>
  </nav>
</template>

<script>
import { inject } from 'vue'
import { useRouter } from 'vue-router'

export default {
  name: 'NavigationBar',
  setup() {
    const appState = inject('appState')
    const router = useRouter()

    const logout = () => {
      appState.isLoggedIn = false
      appState.isSuperuser = false
      localStorage.removeItem('token') // Remove token from local storage
      router.push('/login')
    }

    return {
      appState,
      logout
    }
  }
}
</script>

<style scoped>
.navbar {
  margin-bottom: 20px;
}
</style>
