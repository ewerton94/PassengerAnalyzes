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
              title="Lote 200"
              subtitle="Empresa São Francisco"
            >
            </CardResumo>
            <CardResumo
              itemColor="#f37169"
              iconColor="#f34636"
              iconName="fas fa-route"
              title="716"
              subtitle="Clima Bom / Ponta Verde"
            >
            </CardResumo>
            <CardResumo
              itemColor="#ea6a7f"
              iconColor="#ea4b64"
              iconName="fas fa-user"
              title="14761"
              subtitle="Passageiros"
            >
            </CardResumo>
            <CardResumo
              itemColor="#a270b1"
              iconColor="#9f52b1"
              iconName="bar_chart"
              title="480"
              subtitle="Viagens"
            >
            </CardResumo>
          </div>
        </q-card-section>
      </q-card>
      <div class="row">
        <PassageiroPorDia></PassageiroPorDia>
      </div>

      <div></div>
    </q-page>
    <q-page class="flex flex-center"> </q-page>
  </div>
</template>

<script>
import CardResumo from '../components/Dashboard/CardResumo.vue'
import PassageiroPorDia from '../components/Dashboard/PassageiroPorDia.vue'
export default {
  name: 'PageIndex',
  data: function () {
    return {
    }
  },
  components: {
    CardResumo,
    PassageiroPorDia
  }
}
</script>
