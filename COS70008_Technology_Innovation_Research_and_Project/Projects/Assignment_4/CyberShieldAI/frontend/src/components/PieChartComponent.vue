<template>
  <div class="w-full h-64 flex justify-center items-center">
    <canvas ref="pieChart"></canvas>
  </div>
</template>

<script>
import { Chart, registerables } from 'chart.js';
Chart.register(...registerables);

export default {
  name: 'PieChartComponent',
  props: {
    risk: {
      type: Number,
      required: true
    },
    result: {
      type: String,
      required: true
    }
  },
  mounted() {
    const ctx = this.$refs.pieChart.getContext('2d');
    const isMalware = this.result === 'malware';

    const gradient = ctx.createLinearGradient(0, 0, 0, 400);
    gradient.addColorStop(0, isMalware ? '#dc2626' : '#059669'); // red or green
    gradient.addColorStop(1, isMalware ? '#f87171' : '#34d399'); // lighter red or green

    new Chart(ctx, {
      type: 'doughnut',
      data: {
        labels: [isMalware ? 'Threat Detected' : 'Benign File', 'Remaining'],
        datasets: [{
          data: [this.risk, 100 - this.risk],
          backgroundColor: [gradient, '#e5e7eb'],
          borderWidth: 2,
          borderRadius: 5,
        }]
      },
      options: {
        cutout: '70%',
        plugins: {
          legend: { display: false },
          tooltip: { enabled: false }
        },
        responsive: true,
        maintainAspectRatio: false
      }
    });
  }
};
</script>

<style scoped>
canvas {
  max-width: 100%;
  max-height: 100%;
}
</style>
