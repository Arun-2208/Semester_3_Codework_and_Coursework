<template>
    <nav class="w-full h-[80px] bg-white shadow-sm flex items-center justify-center font-['Calibri']">
      <div class="w-[90%] max-w-[1440px] flex items-center justify-between">
        <!-- Welcome Message -->
        <div class="text-[#4F378A] text-lg font-medium">
          Welcome, {{ username }}
        </div>
  
        <!-- Navigation Tabs -->
        <div class="flex relative right-20 items-center text-[16px] bg-[#EDE4FF] text-black rounded-full">
          <router-link
            to="/dashboard/scan"
            class="px-6 py-3 rounded-tl-full rounded-bl-full"
        
            :class="{
              'bg-[#4F378A] text-white rounded-left': !$route.path.startsWith('/dashboard/scan')
            }"
          >
            Scan
          </router-link>
  
          <router-link
            to="/dashboard/history"
            class="px-6 py-3 "
            :class="{
            
              'bg-[#4F378A] text-white': !$route.path.startsWith('/dashboard/history')
            }"
          >
            Scan History
          </router-link>
  
          <!-- Admin-only Tabs -->
          <router-link
            v-if="userType === 'admin'"
            to="/dashboard/update-model"
            class="px-6 py-3 "
            :class="{
             
              'bg-[#4F378A] text-white': !$route.path.startsWith('/dashboard/update-model')
            }"
          >
            Update Model
          </router-link>
  
          <router-link
            v-if="userType === 'admin'"
            to="/dashboard/analytics"
            class="px-6 py-3 "
            :class="{
           
              'bg-[#4F378A] text-white': !$route.path.startsWith('/dashboard/analytics')
            }"
          >
            Analytics
          </router-link>
  
          <router-link
            to="/dashboard/profile"
            class="px-6 py-3 rounded-r-full"
            :class="{
        
              'bg-[#4F378A] text-white': !$route.path.startsWith('/dashboard/profile')
            }"
          >
            Profile
          </router-link>
        </div>
  
        <!-- Logo and Logout -->
        <div class="flex items-center space-x-4">
          <img src="../assets/logo.jpeg" alt="Logo" class="h-10 w-10 object-contain" />
          <router-link to="/login" @click.native="logout" class="text-[#4F378A] underline text-sm hover:opacity-80">
            Logout
          </router-link>
        </div>
      </div>
    </nav>
  </template>
  
  <script>
  export default {
    name: "Navbar",
    data() {
      return {
        username: "",
        userType: ""
      };
    },
    mounted() {
      const user = JSON.parse(sessionStorage.getItem("user"));
      this.username = user?.username || "User";
      this.userType = user?.user_type || "";
    },
    methods: {
      logout() {
        sessionStorage.clear();
      }
    }
  };
  </script>
  