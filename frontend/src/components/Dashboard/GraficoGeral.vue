<template>
  <q-card class="">
    <q-card-section>
      <div class="text-h6">{{title}}</div>
      <div class="text-subtitle2">{{subtitle}}</div>
    </q-card-section>

    <q-card-section v-if="graficos[tipoGrafico] && dadosObtidos" class="q-pt-none">
      <apexchart
        width="100%"
        :type="modeloGrafico"
        :options="graficos[tipoGrafico].chartOptions"
        :series="graficos[tipoGrafico].series"
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
        tipoGrafico: this.tipoGrafico
      })
      this.dadosObtidos = true
    }
  },
  props: [
    'tipoGrafico',
    'modeloGrafico',
    'title',
    'subtitle'
  ]

}
</script>

<style>
</style>
