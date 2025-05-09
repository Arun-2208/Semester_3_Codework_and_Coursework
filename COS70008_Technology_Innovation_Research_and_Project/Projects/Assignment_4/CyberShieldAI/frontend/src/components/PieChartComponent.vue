<template>
  <div class="w-full h-64">
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
    },
    label: {
      type: String,
      required: true
    },
    malwareType: {
      type: String,
      default: 'benign'
    }
  },
  mounted() {
    const ctx = this.$refs.pieChart.getContext('2d');

    const type = this.malwareType.toLowerCase();
    let color = '#10b981'; // green default

    if (this.result === 'malware') {
      if (type.includes('ransom')) color = '#ef4444'; // red
      else if (type.includes('spy')) color = '#ec4899'; // pink
      else if (type.includes('trojan')) color = '#f97316'; // orange
      else color = '#7c3aed'; // fallback purple
    }

    new Chart(ctx, {
      type: 'pie',
      data: {
        labels: [this.label, 'Remaining'],
        datasets: [
          {
            data: [this.risk, 100 - this.risk],
            backgroundColor: [color, '#f3f4f6'],
            borderWidth: 1
          }
        ]
      },
      options: {
        responsive: true,
        plugins: {
          legend: {
            display: false
          }
        }
      }
    });
  }
};
</script>
