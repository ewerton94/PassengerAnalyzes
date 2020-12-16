<template>
  <div>
    <q-page class="q-pa-sm">
      <q-card class="bg-transparent no-shadow no-border">
        <q-card-section class="q-pa-none">
          <div class="row q-col-gutter-sm">
            <CardResumo
              itemColor="#5064b5"
              iconColor="#3e51b5"
              iconName="fas fa-bus"
              :title="linha.lote"
              :subtitle="linha.empresa"
              :skeleton="!detailComplete"
            >
            </CardResumo>
            <CardResumo
              itemColor="#f37169"
              iconColor="#f34636"
              iconName="fas fa-route"
              :title="linha.numero"
              :subtitle="linha.linha"
              :skeleton="!detailComplete"
            >
            </CardResumo>
            <CardResumo
              itemColor="#ea6a7f"
              iconColor="#ea4b64"
              iconName="fas fa-user"
              :title="linha.passageiros"
              subtitle="Passageiros"
              :skeleton="!detailComplete"
            >
            </CardResumo>
            <CardResumo
              itemColor="#a270b1"
              iconColor="#9f52b1"
              iconName="bar_chart"
              :title="linha.viagens"
              subtitle="Viagens"
              :skeleton="!detailComplete"
            >
            </CardResumo>
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
        ></GraficoGeral>
        </div>
        <div class="col-12 col-md-6 ">

        <GraficoGeral
        class="my-card  col-12 col-md-6 q-ma-sm"
          tipoGrafico = "DadosPorHoraDoDia"
          modeloGrafico = "area"
          title = "Demanda de passageiros"
          subtitle = "Dados por hora do dia"
        ></GraficoGeral>
        </div>
      </div>

      <div></div>
    </q-page>
    <q-page class="flex flex-center"> </q-page>
  </div>
</template>

<script>
import CardResumo from '../components/Dashboard/CardResumo.vue'
import GraficoGeral from '../components/Dashboard/GraficoGeral.vue'
import { mapState, mapActions } from 'vuex'

export default {
  name: 'PageIndex',
  data: function () {
    return {
      detailComplete: false
    }
  },
  created () {
    this.getInfoLinhas()
  },
  computed: {
    ...mapState('Core', ['linha'])
  },
  methods: {
    ...mapActions('Core', ['detalharLinhas']),
    async getInfoLinhas () {
      await this.detalharLinhas(this.$router.currentRoute.query.linhas)
      this.detailComplete = true
    }
  },
  components: {
    CardResumo,
    GraficoGeral
  }
}
</script>
