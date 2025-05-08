<template>
  <div class="w-screen h-screen bg-white flex items-center justify-center overflow-hidden">
    <!-- Main Bounded Container -->
    <div class="w-[90%] max-w-[1440px] h-[90%] flex justify-between items-center relative font-['Calibri']">

      <!-- Left Image Panel -->
      <div class="flex-1 flex justify-center items-center">
        <img
          src="../assets/robot_shield.webp"
          alt="Cyber Bot"
          class="max-h-[600px] w-auto object-contain rounded-xl"
        />
      </div>

      <!-- Right Form Panel -->
      <div class="flex-1 flex flex-col justify-center items-center space-x-8 space-y-6 text-center">
        <!-- Header -->
        <div class="text-2xl text-[#4F378A] mb-4 font-['Calibri']">
          Register and Lets get Going !
        </div>

        <!-- Name Field -->
        <div class="w-full font-['Calibri']">
          <label class="text-sm text-[#4F378A] font-medium">Name</label>
          <input
            v-model="name"
            type="text"
            placeholder="Enter name"
            required
            minlength="3"
            class="w-full h-10 px-4 mt-2 bg-[#F9F9F9] text-[#4F378A] rounded-full border border-gray-300 focus:outline-none font-['Calibri']"
          />
        </div>

        <!-- Email Field -->
        <div class="w-full font-['Calibri']">
          <label class="text-sm text-[#4F378A] font-medium">Email</label>
          <input
            v-model="email"
            type="email"
            placeholder="Enter email"
            required
            class="w-full h-10 px-4 mt-2 bg-[#F9F9F9] text-[#4F378A]  rounded-full border border-gray-300 focus:outline-none font-['Calibri']"
          />
        </div>

        <!-- Password Field -->
        <div class="w-full font-['Calibri']">
          <label class="text-sm text-[#4F378A] font-medium">Password</label>
          <input
            v-model="password"
            type="password"
            placeholder="Enter password"
            required
            minlength="6"
            pattern="^[a-zA-Z0-9@#$%^&+=]+$"
            title="Password must contain only letters, numbers, or @#$%^&+="
            class="w-full h-10 px-4 mt-2 bg-[#F9F9F9] text-[#4F378A] rounded-full border border-gray-300 focus:outline-none font-['Calibri']"
          />
        </div>

        <!-- Admin Checkbox -->
        <div class="w-full flex items-center space-x-2 text-left mt-2">
          <input type="checkbox" v-model="isAdmin" class="accent-[#4F378A]" />
          <label class="text-sm text-gray-800 font-['Calibri']">Admin</label>
        </div>
        <div class="w-full text-left text-xs text-gray-400 font-['Calibri']">Tick box If an Admin</div>

        <!-- Register Button -->
        <button
          @click="register"
          class="w-full h-12 bg-[#4F378A] rounded-full text-white text-xl hover:opacity-90 font-['Calibri']"
        >
          Register
        </button>
      </div>

      <!-- About Us Button -->
      <router-link
        to="/about"
        class="absolute top-6 right-6 px-6 py-2 rounded-full bg-[#F0EFFF] text-[#4F378A] shadow-sm hover:underline text-lg"
      >
        About us
      </router-link>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'RegisterPage',
  data() {
    return {
      name: '',
      email: '',
      password: '',
      isAdmin: false,
    };
  },
  methods: {
    async register() {
      try {
        const res = await axios.post('http://localhost:5000/register', {
          username: this.name,
          email: this.email,
          password: this.password,
          user_type: this.isAdmin ? 'admin' : 'regular',
        });
        sessionStorage.setItem('user', JSON.stringify(res.data));
        this.$router.push('/dashboard/scan');
      } catch (err) {
        alert('Registration failed. Please try again.');
      }
    },
  },
};
</script>
