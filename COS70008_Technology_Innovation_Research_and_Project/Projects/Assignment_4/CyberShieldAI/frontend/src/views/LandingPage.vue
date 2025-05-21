<template>
    <div class="w-screen h-screen bg-white flex items-center justify-center overflow-hidden">
      <!-- Container -->
      <div class="w-[90%] max-w-[1440px] h-[90%] flex justify-between items-center relative font-['Calibri']">
        
        <!-- Left Image -->
        <div class="flex-1 flex justify-center items-center">
          <img
            src="../assets/robot_shield.webp"
            alt="Cyber Bot"
            class="max-h-[600px] w-auto object-contain rounded-xl"
          />
        </div>
  
        <!-- Right Content -->
        <div class="flex-1 flex flex-col justify-center items-center space-y-6 text-center">
          <img
            src="../assets/logo.jpeg"
            alt="Cyber Shield Wheel"
            class="h-[200px] object-contain"
          />
          <div class="text-4xl text-[#4F378A] font-semibold">Cyber Shield AI</div>
          <p class="text-lg text-[#4F378A]">Know the Enemy. Outsmart the Threat.</p>
  
          <!-- Buttons -->
          <div class="flex flex-col space-y-4 w-[200px] mt-4">
            <router-link
              to="/register"
              class="bg-[#65558F] text-white py-2 rounded-full hover:opacity-90"
            >
              Register
            </router-link>
            <router-link
              to="/login"
              class="bg-[#65558F] text-white py-2 rounded-full hover:opacity-90"
            >
              Login
            </router-link>
          </div>
        </div>
  
       
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "LandingPage",
  };
  </script>
  
 