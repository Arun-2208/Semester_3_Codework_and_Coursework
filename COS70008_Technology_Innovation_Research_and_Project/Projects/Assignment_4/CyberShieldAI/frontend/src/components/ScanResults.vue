<template>
    <div class = "w-screen max-w-[1400px] mx-auto mb-[2%]">
    <div class="w-full mx-auto bg-white text-[#65558F] font-['calibri'] relative">
      <!-- Top Bar -->
      <div class="flex justify-between items-center mx-auto m-[1%] px-[4%] text-xl cursor-pointer hover:underline">
        <div>Welcome, Ragav</div>
        <div class="cursor-pointer hover:underline">Logout</div>
      </div>
  
      <!-- Header Bar -->
      <div class="w-full  mx-auto mt-[1%] h-[10vh] bg-[#4F378A] rounded-[150px] flex items-center shadow-md px-[2%]">
        <img src="./logo.jpeg" alt="logo" class="h-[90%] aspect-square rounded-full object-cover" />
        <div class="flex justify-between items-center w-full ml-[2%]">
          <div class="bg-[#EADDFF] text-black px-[2vw] py-[0.8vh] rounded-full text-[1.1vw] font-medium">Scan</div>
          <div class="text-white px-[2vw] py-[0.8vh] text-[1.1vw] hover:underline cursor-pointer">Scan History</div>
          <div class="text-white px-[2vw] py-[0.8vh] text-[1.1vw] hover:underline cursor-pointer">Update Dataset & Retrain Model</div>
          <div class="text-white px-[2vw] py-[0.8vh] text-[1.1vw] hover:underline cursor-pointer">Analytics Dashboard</div>
        </div>
      </div>
  
      <!-- Center Title -->
      <div class="text-[2.5vw] font-semibold text-center mt-[4vh]">Scan Results</div>
  
      <!-- Panels Container -->
      <div class="flex justify-between item-center w-[90%] mx-auto mt-[3vh] flex-wrap">
        <!-- Left Panel -->
        <div class="flex flex-col  justify -between items-center w-[40%] bg-white rounded-[2vw] shadow-md p-[2%]">
          <div class="text-[2.5vw] text-[#E00E11] font-bold mb-[4vh]">Malware</div>
          <div class="text-[1.5vw] text-[#E00E11] mb-[4vh]">Trojan Horse</div>
          <div class="text-[1.2vw] text-[#E00E11] bg-[#FFE6E6] rounded-full w-full py-[1.2vh] text-center mb-[4vh]">Suspicious Behaviour: 76%</div>
          <div class="text-[1.2vw] text-[#E00E11] bg-[#FFE6E6] rounded-full w-full py-[1.2vh] text-center mb-[4vh]">Prediction Strength: 89%</div>
          <div class="text-[1vw] text-[#E00E11] bg-[#FFE6E6] rounded-full w-full py-[1.2vh] px-[2%] text-center mb-[4vh]">
            Suggested Action: Trojan detected. It may disguise as safe software. Avoid execution.
          </div>
          <div class="flex justify-between w-full mt-auto gap-[2%]">
            <button class="w-1/2 py-[1.5vh] bg-[#F51515] rounded-full text-white text-[1vw] font-medium hover:opacity-90">Download PDF</button>
            <button class="w-1/2 py-[1.5vh] bg-[#28AF2D] rounded-full text-white text-[1vw] font-medium hover:opacity-90">Download CSV</button>
          </div>
        </div>
  
        <!-- Right Panel -->
        <div class="flex flex-col items-center w-[40%]">
          <div class="bg-[#4F378A] w-[50%] h-[6vh] rounded-full flex items-center justify-center mb-[2vh]">
            <div class="text-white text-[1.5vw] font-medium">Threat Level</div>
          </div>
          <div class="w-[70%] aspect-square">
            <svg viewBox="0 0 362 362" fill="none" xmlns="http://www.w3.org/2000/svg" class="w-full h-full">
              <path d="M181 181V1C280.412 1 361 81.5887 361 181C361 280.411 280.412 361 181 361C131.299 361 83.8094 340.449 49.7863 304.219L181 181Z" fill="#F5AE15" stroke="white" />
              <path d="M181 181L49.7861 304.218C-18.2655 231.751 -14.6856 117.837 57.782 49.7856C91.1559 18.4454 135.218 1 181 1V181Z" fill="#F5F5F5" stroke="white" />
            </svg>
          </div>
          <div class="bg-[#F5AE15] w-[50%] h-[6vh] rounded-full flex items-center justify-center mt-[2vh]">
            <div class="text-white text-[1.5vw] font-medium">Moderate Risk</div>
          </div>
          <button class="w-[80%] h-[7vh] bg-[#65558F] rounded-[2vw] mt-[3vh] text-white text-[1.8vw] font-semibold hover:opacity-90">
            Scan Again
          </button>
        </div>
      </div>
    </div>
</div>
  </template>
  
  <script>
  export default {
    name: 'ScanResults'
  }
  </script>
  
  <style scoped>
  /* Fully responsive and modular layout */
  </style>
  