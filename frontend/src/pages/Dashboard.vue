<template>
  <div >
    <q-page class="q-pa-sm">
      <q-card class="bg-transparent no-shadow no-border">
        <q-card-section class="q-pa-none">
          <Filtro/>
        </q-card-section>
      </q-card>
      <div :key="geralKey">
      <q-card  class="bg-transparent no-shadow no-border">
        <q-card-section class="q-pa-none">
          <div class="row q-col-gutter-sm">
            <CardResumo itemColor="#5064b5" iconColor="#3e51b5" iconName="fas fa-bus" :title="linha.lote" :subtitle="linha.empresa"/>
            <CardResumo itemColor="#f37169" iconColor="#f34636" iconName="fas fa-route" :title="linha.numero" :subtitle="linha.linha"/>
            <CardResumo  itemColor="#ea6a7f"  iconColor="#ea4b64"  iconName="fas fa-user"  :title="linha.passageiros"  subtitle="Passageiros"/>
            <CardResumo  itemColor="#a270b1"  iconColor="#9f52b1"  iconName="bar_chart"  :title="linha.viagens"  subtitle="Viagens"/>
          </div>
        </q-card-section>
      </q-card>
      <div class="row">
        <div class="col-12 col-md-6 ">
        <GraficoGeral
          class="my-card   q-ma-sm"
          tipoGrafico = "DadosPorDiaDaSemana"
          modeloGrafico = "bar"
          title = "Demanda de passageiros"
          subtitle = "Dados por dia da semana"
          :timeout="1"
        ></GraficoGeral>
        </div>
        <div class="col-12 col-md-6 ">

        <GraficoGeral
        class="my-card  col-12 col-md-6 q-ma-sm"
          tipoGrafico = "DadosPorHoraDoDia"
          modeloGrafico = "area"
          title = "Demanda de passageiros"
          subtitle = "Dados por hora do dia"
          :timeout="1"
        ></GraficoGeral>

        </div>
        <div class="col-12 col-md-12 ">

        <GraficoPlotly
        class="my-card  col-12 col-md-12 q-ma-sm"
          tipoGrafico = "BoxPlotPorTrecho"
          modeloGrafico = "box"
          divId="plot1"
          title = "Embarque de passageiros"
          subtitle = "Dados por Trecho/Viagem"
          :timeout="2"
        ></GraficoPlotly>
        <GraficoPlotly
          class="my-card  col-12 col-md-12 q-ma-sm"
          tipoGrafico = "BoxPlotPorTrechoDesembarque"
          modeloGrafico = "box"
          divId="plot2"
          title = "Desembarque de passageiros"
          subtitle = "Dados por Trecho/Viagem"
          :timeout="3"
        ></GraficoPlotly>

        <GraficoGoogle
        class="my-card  col-12 col-md-12 q-ma-sm"
          tipoGrafico = "SankeyOD"
          modeloGrafico = "box"
          title = "Fluxo O/D de passageiros"
          subtitle = "Contagem no período"
          :timeout="4"
        ></GraficoGoogle>
        <MapaCalor
        class="my-card  col-12 col-md-12 q-ma-sm"
          tipoGrafico = "MapaCalorEmbarque"
          modeloGrafico = "box"
          title = "Localização de passageiros"
          subtitle = "Mapa de calor"
          :timeout="4"
        ></MapaCalor>
        </div>
      </div>
      </div>

      <div></div>
    </q-page>
    <q-page class="flex flex-center"> </q-page>
  </div>
</template>

<script>
import Filtro from '../components/Dashboard/Filtro.vue'
import CardResumo from '../components/Dashboard/CardResumo.vue'
import GraficoGeral from '../components/Dashboard/GraficoGeral.vue'
import GraficoPlotly from '../components/Dashboard/GraficoPlotly.vue'
import GraficoGoogle from '../components/Dashboard/GraficoGoogle.vue'
import MapaCalor from '../components/Dashboard/MapaCalor.vue'
import { mapState, mapActions, mapMutations } from 'vuex'

export default {
  name: 'PageIndex',
  data: function () {
    return {

    }
  },
  mounted () {
    this.getInfoLinhas()
  },
  computed: {
    ...mapState('Core', ['linha', 'extraFiltro', 'geralKey', 'detailComplete'])
  },
  methods: {
    ...mapActions('Core', ['detalharLinhas']),
    ...mapMutations('Core', ['ADD_EXTRA_FILTRO_INICIAL', 'SET_ENDED']),
    async getInfoLinhas () {
      await this.ADD_EXTRA_FILTRO_INICIAL({ newExtraFiltroKey: 'linhas', newExtraFiltroValue: this.$router.currentRoute.query.linhas })
      await this.detalharLinhas(this.extraFiltro)
    }
  },
  components: {
    CardResumo,
    Filtro,
    GraficoGeral,
    GraficoPlotly,
    GraficoGoogle,
    MapaCalor
  }
}
</script>
