<template>
  <q-card :key="key" class="">
    <q-card-section>
      <div class="text-h6">{{title}}</div>
      <div class="text-subtitle2">{{subtitle}}</div>

    </q-card-section>

    <q-card-section v-if="graficos[tipoGrafico] && dadosObtidos" class="q-pt-none">
      <GChart
    type="Sankey"
    :data="graficos[tipoGrafico].data"
    :options="graficos[tipoGrafico].layout"
    :settings="{ packages: ['sankey'] }"
  />
    </q-card-section>
    <q-card-section v-if="!dadosObtidos" class="q-pt-none">
      <q-skeleton height="300px" square />
    </q-card-section>

  </q-card>
</template>

<script>
import { GChart } from 'vue-google-charts'

import { mapState, mapActions, mapMutations } from 'vuex'
export default {
  name: 'PassageiroPorDia',

  data: function () {
    return {
      dadosObtidos: false,
      key: 0

    }
  },
  components: {
    GChart
  },
  computed: {
    ...mapState('Core', ['graficos', 'extraFiltro'])
  },
  created () {
    this.start()
  },
  methods: {
    ...mapActions('Core', ['obterDadosGrafico']),
    ...mapMutations('Core', ['ADD_NEW_EXTRA_FILTRO']),
    async start () {
      // await this.ADD_NEW_EXTRA_FILTRO({ newExtraFiltroKey: 'linhas', newExtraFiltroValue: this.$router.currentRoute.query.linhas })
      var extraFiltro = await this.extraFiltro
      // console.log(extraFiltro)
      extraFiltro = JSON.parse(JSON.stringify(extraFiltro))
      extraFiltro.tipo_grafico = this.tipoGrafico
      await this.obterDadosGrafico(extraFiltro)
      this.dadosObtidos = true
      this.key = this.key + 1
      // console.log(this.graficos)
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
