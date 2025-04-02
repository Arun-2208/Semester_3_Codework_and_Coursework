<template>
    <div class="w-[1880px] mx-auto bg-white relative text-[#65558F] font-['Roboto']">
      <!-- Top Bar -->
      <div class="absolute top-[222px] left-[36px] text-2xl text-center">Welcome , Ragav</div>
      <div class="absolute top-[220px] right-[36px] text-2xl text-center">Logout</div>
  
      <!-- Header Bar -->
      <div class="absolute top-[36px] left-1/2 -translate-x-1/2 w-[1808px] h-[150px] bg-[#4F378A] rounded-[150px] flex items-center justify-between px-[36px]">
        <img src="./logo.jpeg" alt="logo" class="w-[152px] h-[150px] rounded-[150px] object-cover" />
        <div class="flex space-x-12 text-white text-2xl">
          <div class="bg-[#EADDFF] text-black px-8 py-4 rounded-full">Scan</div>
          <div class="px-8 py-4">Scan History</div>
          <div class="px-8 py-4">Update Dataset & Retrain Model</div>
          <div class="px-8 py-4">Analytics Dashboard</div>
        </div>
      </div>
  
      <!-- Left Panel -->
      <div class="absolute top-[392px] left-[108px] w-[675px] h-[900px] bg-white rounded-[25px] shadow-md p-6 flex flex-col items-center">
        <div class="text-[57px] text-[#E00E11] mb-4">Malware</div>
        <div class="text-4xl text-[#E00E11] mb-2">Trojan Horse</div>
        <div class="text-4xl text-[#E00E11] bg-[#FFE6E6] rounded-[50px] w-[600px] py-4 text-center mb-2">Suspicious Behaviour : 76 %</div>
        <div class="text-4xl text-[#E00E11] bg-[#FFE6E6] rounded-[50px] w-[600px] py-4 text-center mb-2">Prediction strength : 89 %</div>
        <div class="text-2xl text-[#E00E11] bg-[#FFE6E6] rounded-[50px] w-[600px] py-4 text-center mb-4">
          Suggested User Action : Trojan detected. It may disguise as safe software. Avoid execution.
        </div>
        <div class="flex justify-between w-full px-6 mt-auto">
          <button class="w-[240px] h-[70px] bg-[#F51515] rounded-[50px] text-white text-2xl">Download PDF</button>
          <button class="w-[240px] h-[70px] bg-[#28AF2D] rounded-[50px] text-white text-2xl">Download CSV</button>
        </div>
      </div>
  
      <!-- Right Panel: Scan Results -->
      <div class="absolute top-[392px] right-[108px] text-center">
        <div class="bg-[#4F378A] w-[300px] h-[70px] rounded-[50px] flex items-center justify-center mb-4">
          <div class="text-white text-4xl">Threat level</div>
        </div>
        <div class="w-[362px] h-[362px] mx-auto">
          <svg width="362" height="362" viewBox="0 0 362 362" fill="none" xmlns="http://www.w3.org/2000/svg">
            <path d="M181 181V1C280.412 1 361 81.5887 361 181C361 280.411 280.412 361 181 361C131.299 361 83.8094 340.449 49.7863 304.219L181 181Z" fill="#F5AE15" stroke="white" />
            <path d="M181 181L49.7861 304.218C-18.2655 231.751 -14.6856 117.837 57.782 49.7856C91.1559 18.4454 135.218 1 181 1V181Z" fill="#F5F5F5" stroke="white" />
          </svg>
        </div>
        <div class="bg-[#F5AE15] w-[300px] h-[70px] rounded-[50px] flex items-center justify-center mt-4">
          <div class="text-white text-4xl">Moderate Risk</div>
        </div>
        <div class="bg-[#65558F] w-[550px] h-[90px] rounded-[30px] mt-6 flex items-center justify-center">
          <div class="text-white text-[45px]">Scan Again</div>
        </div>
      </div>
  
      <!-- Center Title -->
      <div class="absolute top-[370px] left-1/2 -translate-x-1/2 text-[57px] text-[#65558F] text-center">
        Scan Results
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'ScanResults'
  }
  </script>
  
  <style scoped>
  /* Fully responsive using Tailwind */
  </style>
  