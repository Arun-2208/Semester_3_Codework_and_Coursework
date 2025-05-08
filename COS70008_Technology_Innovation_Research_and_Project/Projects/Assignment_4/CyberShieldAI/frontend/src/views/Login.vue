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
        <div class=" flex-1 flex flex-col justify-center items-center space-x-8 space-y-6 text-center">

          <!-- Header -->
          <div class="text-2xl text-[#4F378A] text-center mb-8 font-['Calibri']">
            Login and Lets get Going !
          </div>
  
          <!-- Email Field -->
          <div class="w-full mb-4 font-['Calibri']">
            <label class="text-sm text-[#4F378A] font-medium">Email</label>
            <input
              v-model="email"
              type="email"
              placeholder="Enter email"
              class="w-full h-10 px-4 mt-2 bg-[#F9F9F9] text-[#4F378A] rounded-full border border-gray-300 focus:outline-none font-['Calibri']"
            />
          </div>
  
          <!-- Password Field -->
          <div class="w-full mb-4 font-['Calibri']">
            <label class="text-sm text-[#4F378A] font-medium">Password</label>
            <input
              v-model="password"
              type="password"
              placeholder="Enter password"
              class="w-full h-10 px-4 mt-2 bg-[#F9F9F9] text-[#4F378A] rounded-full border border-gray-300 focus:outline-none font-['Calibri']"
            />
          </div>
  
          <!-- Forgot Password -->
          <div class="w-full text-right mb-6">
            <a href="#" class="text-sm text-[#4F378A] underline font-['Calibri']">Forgot password</a>
          </div>
  
          <!-- Login Button -->
          <button
            @click="login"
            class="w-full h-12 bg-[#4F378A] rounded-full text-white text-xl hover:opacity-90 font-['Calibri']"
          >
            Login
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
  name: 'LoginPage',
  data() {
    return {
      email: '',
      password: ''
    };
  },
  methods: {
    async login() {
      try {
        const res = await axios.post('http://localhost:5000/login', {
          email: this.email,
          password: this.password
        });

        sessionStorage.setItem('user', JSON.stringify(res.data));
        this.$router.push('/dashboard/scan');
      } catch (err) {
        alert('Login failed. Please check your credentials.');
      }
    }
  }
};
</script>
  