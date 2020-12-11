<template>
  <q-card class="my-card q-mt-md col-12 col-md-6">
    <q-card-section>
      <div class="text-h6">Demanda de passageiros</div>
      <div class="text-subtitle2">Por dia da semana</div>
    </q-card-section>

    <q-card-section class="q-pt-none">
      <apexchart
        width="100%"
        type="bar"
        :options="chartOptions"
        :series="series"
      ></apexchart>
    </q-card-section>
  </q-card>
</template>

<script>
export default {
  name: 'PassageiroPorDia',
  data: function () {
    return {
      chartOptions: {
        chart: {
          id: 'vuechart-example'
        },
        xaxis: {
          categories: [
            'Segunda-Feira',
            'Terça-Feira',
            'Quarta-Feira',
            'Quinta-Feira',
            'Sexta-Feira'
          ]
        }
      },
      series: [
        {
          name: 'series-1',
          data: [2995, 2967, 2846, 3003, 2949]
        }
      ]
    }
  }
}
</script>

<style>
</style>
