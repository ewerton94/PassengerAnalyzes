<template>
  <q-card :key="key" class="">
    <q-card-section>
      <div class="text-h6">{{title}}</div>
      <div class="text-subtitle2">{{subtitle}}</div>

    </q-card-section>

    <q-card-section  class="q-pt-none q-pa-none q-ma-none">
      <div :ref="divId" :id="divId"></div>

      <!--<Plotly  :ref="divId" :data="graficos[tipoGrafico].data" :layout="graficos[tipoGrafico].layout" ></Plotly>-->
    </q-card-section>
    <q-card-section v-show="!dadosObtidos" class="q-pt-none">
      <q-skeleton height="300px" square />
    </q-card-section>

  </q-card>
</template>

<script>
import Plotly from 'plotly.js-dist'
import { mapState, mapActions, mapMutations } from 'vuex'
export default {
  name: 'PassageiroPorDia',

  data: function () {
    return {
      dadosObtidos: false,
      key: 0

    }
  },
  computed: {
    ...mapState('Core', ['graficos', 'extraFiltro'])
  },

  created () {
    this.start()
  },
  onEnd: function () {
    // when you want to reload the component just make `loaded = false`
    this.dadosObtidos = false
    console.log('Aqui aaaaaaaaaaaaaaaa')
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
      // console.log('this.divId')
      // console.log(this.divId)
      this.$nextTick(() => {
        const el = this.$refs[this.divId]
        // console.log('EL')
        // console.log(el)
        var layout = this.graficos[this.tipoGrafico].layout
        if (this.$q.screen.lt.md) {
          layout.showlegend = false
          layout.margin = {
            l: 0,
            r: 0,
            b: 0,
            t: 0,
            pad: 4
          }
          layout.yaxis = Object.assign({}, layout.yaxis, { fixedrange: true })
          layout.xaxis = Object.assign({}, layout.xaxis, { fixedrange: true })
        }
        Plotly.newPlot(el, this.graficos[this.tipoGrafico].data, layout, { responsive: true })
      // this.key = this.key + 1
      })

      // console.log('this.graficos plorty')
      // console.log(this.graficos)
    }
  },
  props: [
    'tipoGrafico',
    'modeloGrafico',
    'title',
    'subtitle',
    'divId',
    'timeout'
  ]

}
</script>

<style>
</style>
