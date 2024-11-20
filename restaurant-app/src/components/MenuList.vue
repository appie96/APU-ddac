<template>
  <div class="menu-container">
    <h1 class="title">Our Menu</h1>
    <div v-if="loading" class="loading">
      <div class="loading-spinner"></div>
      Loading menu items...
    </div>
    <div v-else-if="error" class="error-message">
      {{ error }}
      <button @click="retryFetch" class="retry-button">Try Again</button>
    </div>
    <div v-else class="menu-grid">
      <div
        v-for="item in menuItems"
        :key="item.id"
        class="menu-card"
      >
        <img
          :src="item.image_url"
          :alt="item.name"
          class="menu-image"
          @error="handleImageError"
        />
        <div class="menu-info">
          <h2 class="menu-name">{{ item.name }}</h2>
          <p class="menu-description">{{ item.description }}</p>
          <p class="menu-price">${{ item.price }}</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

const CONFIG = {
  API_URL: 'https://gy3d55i8pc.execute-api.us-east-1.amazonaws.com/menu',
  TIMEOUT: 5000
};

export default {
  name: 'MenuList',
  data() {
    return {
      menuItems: [],
      loading: true,
      error: null
    };
  },
  methods: {
    fetchMenuItems() {
      this.loading = true;
      this.error = null;
      axios.get(CONFIG.API_URL, { timeout: CONFIG.TIMEOUT })
        .then(response => {
          this.menuItems = response.data;
          this.loading = false;
        })
        .catch(() => {
          this.error = 'Failed to load menu items. Please try again later.';
          this.loading = false;
        });
    },
    retryFetch() {
      this.fetchMenuItems();
    },
    handleImageError(event) {
      event.target.src = 'path/to/default-image.jpg'; // Provide a default image path
    }
  },
  mounted() {
    this.fetchMenuItems();
  }
};
</script>

<style scoped>
.menu-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
  text-align: center;
}

.loading {
  text-align: center;
  padding: 40px;
  color: #666;
}

.loading-spinner {
  border: 4px solid #f3f3f3;
  border-top: 4px solid #3498db;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  animation: spin 1s linear infinite;
  margin: 0 auto 20px;
}

.error-message {
  text-align: center;
  padding: 20px;
  color: #dc3545;
}

.retry-button {
  margin-top: 10px;
  padding: 8px 16px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.retry-button:hover {
  background-color: #0056b3;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.title {
  font-size: 2.5rem;
  margin-bottom: 20px;
  color: #333;
}

.menu-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(250px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.menu-card {
  background: #fff;
  border-radius: 10px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  text-decoration: none; /* Remove underline */
  color: inherit; /* Inherit text color */
}

.menu-card:hover {
  transform: translateY(-10px);
  box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
}

.menu-image {
  width: 100%;
  height: 200px;
  object-fit: cover;
}

.menu-info {
  padding: 15px;
}

.menu-name {
  font-size: 1.5rem;
  color: #333;
  margin-bottom: 5px;
}

.menu-price {
  font-size: 1.2rem;
  color: #666;
}

.menu-description {
  color: #666;
  font-size: 0.9rem;
  margin: 8px 0;
}

/* Media queries for responsive design */
@media (min-width: 600px) {
  .menu-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 599px) {
  .menu-grid {
    grid-template-columns: 1fr;
  }
}
</style>
