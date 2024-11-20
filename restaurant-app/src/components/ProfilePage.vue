<template>
  <div class="profile-page container mt-5">
    <div v-if="loading" class="text-center">
      <div class="spinner-border text-primary" role="status">
        <span class="visually-hidden">Loading...</span>
      </div>
    </div>

    <div v-else-if="error" class="alert alert-danger">
      {{ error }}
    </div>

    <div v-else>
      <h1 class="text-center mb-4">Profile</h1>
      <form @submit.prevent="updateProfile">
        <div class="mb-3">
          <label for="name" class="form-label">Name</label>
          <input
            type="text"
            id="name"
            v-model="user.name"
            class="form-control"
            required
          />
        </div>
        <div class="mb-3">
          <label for="email" class="form-label">Email</label>
          <input
            type="email"
            id="email"
            v-model="user.email"
            class="form-control"
            required
            disabled
          />
        </div>
        <button type="submit" class="btn btn-primary" :disabled="isSubmitting">
          {{ isSubmitting ? 'Updating...' : 'Update Profile' }}
        </button>
      </form>

      <h2 class="mt-5 mb-4">My Reservations</h2>
      <div v-if="loadingReservations" class="text-center">
        <div class="spinner-border text-primary" role="status">
          <span class="visually-hidden">Loading reservations...</span>
        </div>
      </div>
      <div v-else-if="reservationError" class="alert alert-danger">
        {{ reservationError }}
      </div>
      <div v-else-if="reservations.length === 0" class="text-center">
        <p>No reservations found.</p>
      </div>
      <div v-else>
        <table class="table">
          <thead>
            <tr>
              <th>Date</th>
              <th>Time</th>
              <th>Guests</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="reservation in reservations" :key="reservation.id">
              <td>{{ reservation.date }}</td>
              <td>{{ reservation.time }}</td>
              <td>{{ reservation.guests }}</td>
              <td>{{ reservation.status }}</td>
              <td>
                <router-link 
                  :to="{ name: 'ReservationEdit', query: { reservation_id: reservation.id }}" 
                  class="btn btn-sm btn-warning me-2">Edit</router-link>
                <button 
                  @click="cancelReservation(reservation.id)" 
                  class="btn btn-sm btn-danger">Cancel</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  name: 'ProfilePage',
  data() {
    return {
      user: {
        name: "",
        email: ""
      },
      reservations: [],
      loading: true,
      loadingReservations: true,
      error: null,
      reservationError: null,
      isSubmitting: false
    };
  },
  methods: {
    async fetchUserData() {
      const token = localStorage.getItem("token");
      if (!token) {
        this.$router.push('/login');
        return;
      }

      try {
        const response = await axios.get("/api/users/me/", {
          headers: { 
            Authorization: `Bearer ${token}`
          }
        });
        
        console.log("User data response:", response.data);
        this.user = response.data;
        this.loading = false;
      } catch (error) {
        console.error("Failed to fetch user data:", error.response?.data || error.message);
        this.error = "Failed to load profile data. Please try again later.";
        this.loading = false;
        if (error.response?.status === 401) {
          localStorage.removeItem('token');
          this.$router.push('/login');
        }
      }
    },

    async updateProfile() {
      this.isSubmitting = true;
      const token = localStorage.getItem("token");
      
      try {
        await axios.patch("/api/users/me/", 
          { name: this.user.name },
          {
            headers: { 
              Authorization: `Bearer ${token}`,
              'Content-Type': 'application/json'
            }
          }
        );
        alert("Profile updated successfully!");
      } catch (error) {
        console.error("Failed to update profile:", error);
        alert("Failed to update profile. Please try again.");
      } finally {
        this.isSubmitting = false;
      }
    },

    async fetchReservations() {
      const token = localStorage.getItem("token");
      if (!token) {
        this.$router.push('/login');
        return;
      }

      try {
        const response = await axios.get("/api/reservations/my/", {
          headers: { 
            Authorization: `Bearer ${token}`
          }
        });
        
        console.log("Reservations data:", response.data);
        this.reservations = response.data;
        this.loadingReservations = false;
      } catch (error) {
        console.error("Failed to fetch reservations:", error.response?.data || error.message);
        this.reservationError = "Failed to load reservations. Please try again later.";
        this.loadingReservations = false;
      }
    },

    async cancelReservation(id) {
      if (confirm("Are you sure you want to cancel this reservation?")) {
        const token = localStorage.getItem("token");
        if (!token) {
          this.$router.push('/login');
          return;
        }

        try {
          await axios.delete(`/api/reservations/${id}/`, {
            headers: { Authorization: `Bearer ${token}` }
          });
          alert("Reservation canceled successfully!");
          this.fetchReservations();
        } catch (error) {
          console.error("Failed to cancel reservation:", error);
          alert("Failed to cancel reservation. Please try again.");
        }
      }
    }
  },
  async mounted() {
    await this.fetchUserData();
    await this.fetchReservations();
  }
};
</script>

<style scoped>
.container {
  max-width: 800px;
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
@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}
</style>