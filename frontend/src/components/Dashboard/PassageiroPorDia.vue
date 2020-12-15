<template>
  <q-card class="my-card q-mt-md col-12 col-md-6">
    <q-card-section>
      <div class="text-h6">Demanda de passageiros</div>
      <div class="text-subtitle2">Por dia da semana</div>
    </q-card-section>

    <q-card-section v-if="graficos.DadosPorDiaDaSemana && dadosObtidos" class="q-pt-none">
      <apexchart
        width="100%"
        type="bar"
        :options="graficos.DadosPorDiaDaSemana.chartOptions"
        :series="graficos.DadosPorDiaDaSemana.series"
      ></apexchart>
    </q-card-section>
    <q-card-section v-if="!dadosObtidos" class="q-pt-none">
      <q-skeleton height="300px" square />
    </q-card-section>

  </q-card>
</template>

<script>
import { mapState, mapActions } from 'vuex'
export default {
  name: 'PassageiroPorDia',

  data: function () {
    return {
      dadosObtidos: false

    }
  },
  computed: {
    ...mapState('Core', ['graficos'])
  },
  created () {
    this.start()
  },

  methods: {
    ...mapActions('Core', ['obterDadosGrafico']),
    async start () {
      await this.obterDadosGrafico({
        linhas: this.$router.currentRoute.query.linhas,
        tipoGrafico: 'DadosPorDiaDaSemana'
      })
      this.dadosObtidos = true
    }
  }

}
</script>

<style>
</style>
