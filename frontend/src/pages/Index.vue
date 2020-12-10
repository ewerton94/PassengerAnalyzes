<template>
<div>
  <q-page class="q-pa-sm">
    <q-card class="bg-transparent no-shadow no-border">
      <q-card-section class="q-pa-none">
        <div class="row q-col-gutter-sm ">
          <div class="col-md-3 col-sm-12 col-xs-12">
            <q-item style="background-color: #5064b5" class="q-pa-none q-ml-xs">
              <q-item-section side style="background-color: #3e51b5" class=" q-pa-lg q-mr-none text-white">
                <q-icon name="fas fa-bus" color="white" size="24px"></q-icon>
              </q-item-section>
              <q-item-section class=" q-pa-md q-ml-none  text-white">
                <q-item-label class="text-white text-h6 text-weight-bolder">Lote 200</q-item-label>
                <q-item-label>Empresa São Francisco</q-item-label>
              </q-item-section>
            </q-item>
          </div>
          <div class="col-md-3 col-sm-12 col-xs-12">
            <q-item style="background-color: #f37169" class="q-pa-none q-ml-xs ">
              <q-item-section side style="background-color: #f34636" class=" q-pa-lg q-mr-none text-white">
                <q-icon name="fas fa-route" size="24px"></q-icon>
              </q-item-section>
              <q-item-section class=" q-pa-md q-ml-none  text-white">
                <q-item-label class="text-white text-h6 text-weight-bolder">716</q-item-label>
                <q-item-label>Clima Bom / Ponta Verde</q-item-label>
              </q-item-section>
            </q-item>
          </div>
          <div class="col-md-3 col-sm-12 col-xs-12">
            <q-item style="background-color: #ea6a7f" class="q-pa-none q-ml-xs">
              <q-item-section side style="background-color: #ea4b64" class=" q-pa-lg q-mr-none text-white">
                <q-icon name="fas fa-user" size="24px"></q-icon>
              </q-item-section>
              <q-item-section class=" q-pa-md q-ml-none  text-white">
                <q-item-label class="text-white text-h6 text-weight-bolder">14761</q-item-label>
                <q-item-label>Passageiros</q-item-label>
              </q-item-section>
            </q-item>
          </div>
          <div class="col-md-3 col-sm-12 col-xs-12">
            <q-item style="background-color: #a270b1" class="q-pa-none q-ml-xs q-mr-xs">
              <q-item-section side style="background-color: #9f52b1" class=" q-pa-lg q-mr-none text-white">
                <q-icon name="bar_chart" size="24px"></q-icon>
              </q-item-section>
              <q-item-section class=" q-pa-md q-ml-none  text-white">
                <q-item-label class="text-white text-h6 text-weight-bolder">480</q-item-label>
                <q-item-label>Viagens</q-item-label>
              </q-item-section>
            </q-item>
          </div>
        </div>
      </q-card-section>
    </q-card>
    <div class="row">
      <q-card class="my-card q-mt-md col-12 col-md-6">

      <q-card-section>
        <div class="text-h6">Demanda de passageiros</div>
        <div class="text-subtitle2">Por dia da semana</div>
      </q-card-section>

      <q-card-section class="q-pt-none">
        <apexchart width="100%" type="bar" :options="chartOptions" :series="series"></apexchart>
      </q-card-section>
    </q-card>

    </div>

    <div>

   </div>
  </q-page>
  <q-page class="flex flex-center">

  </q-page>
  </div>
</template>

<script>

export default {
  name: 'PageIndex',
  data: function () {
    return {
      chartOptions: {
        chart: {
          id: 'vuechart-example'
        },
        xaxis: {
          categories: ['Segunda-Feira', 'Terça-Feira', 'Quarta-Feira', 'Quinta-Feira', 'Sexta-Feira']
        }
      },
      series: [{
        name: 'series-1',
        data: [2995, 2967, 2846, 3003, 2949]
      }]
    }
  }
}
</script>
